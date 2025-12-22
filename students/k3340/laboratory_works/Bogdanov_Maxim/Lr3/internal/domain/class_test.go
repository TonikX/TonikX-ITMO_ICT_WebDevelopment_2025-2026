package domain

import (
	"testing"
	"time"

	mockclock "school-service/internal/infrastructure/clock"
)

func TestNewClass(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))

	tests := []struct {
		name           string
		grade          int
		letter         string
		academicYearID int
		classTeacherID *int
		wantErr        bool
	}{
		{
			name:           "valid class",
			grade:          9,
			letter:         "A",
			academicYearID: 1,
			classTeacherID: nil,
			wantErr:        false,
		},
		{
			name:           "valid class with teacher",
			grade:          10,
			letter:         "B",
			academicYearID: 1,
			classTeacherID: intPtr(1),
			wantErr:        false,
		},
		{
			name:           "grade too low",
			grade:          0,
			letter:         "A",
			academicYearID: 1,
			classTeacherID: nil,
			wantErr:        true,
		},
		{
			name:           "grade too high",
			grade:          12,
			letter:         "A",
			academicYearID: 1,
			classTeacherID: nil,
			wantErr:        true,
		},
		{
			name:           "empty letter",
			grade:          9,
			letter:         "",
			academicYearID: 1,
			classTeacherID: nil,
			wantErr:        true,
		},
		{
			name:           "letter too long",
			grade:          9,
			letter:         "ABCDEF",
			academicYearID: 1,
			classTeacherID: nil,
			wantErr:        true,
		},
		{
			name:           "invalid academicYearID",
			grade:          9,
			letter:         "A",
			academicYearID: 0,
			classTeacherID: nil,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			class, err := NewClass(mockClock, tt.grade, tt.letter, tt.academicYearID, tt.classTeacherID)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				if class != nil {
					t.Errorf("expected nil class, got %v", class)
				}
			} else {
				if err != nil {
					t.Errorf("unexpected error: %v", err)
				}
				if class == nil {
					t.Fatal("expected non-nil class")
				}
				if class.Grade() != tt.grade {
					t.Errorf("expected Grade = %d, got %d", tt.grade, class.Grade())
				}
				if class.Letter() != tt.letter {
					t.Errorf("expected Letter = %s, got %s", tt.letter, class.Letter())
				}
				if class.AcademicYearID() != tt.academicYearID {
					t.Errorf("expected AcademicYearID = %d, got %d", tt.academicYearID, class.AcademicYearID())
				}
			}
		})
	}
}

func TestRestoreClassFromDB(t *testing.T) {
	now := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	teacherID := 1

	class := RestoreClassFromDB(1, 9, "A", 1, &teacherID, now, now, nil)

	if class.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", class.ID())
	}
	if class.Grade() != 9 {
		t.Errorf("expected Grade = 9, got %d", class.Grade())
	}
	if class.Letter() != "A" {
		t.Errorf("expected Letter = A, got %s", class.Letter())
	}
	if *class.ClassTeacherID() != teacherID {
		t.Errorf("expected ClassTeacherID = %d, got %d", teacherID, *class.ClassTeacherID())
	}
	if !timeEqual(class.CreatedAt(), now) {
		t.Errorf("expected CreatedAt = %v, got %v", now, class.CreatedAt())
	}
	if class.IsDeleted() {
		t.Error("expected IsDeleted = false")
	}
}

func TestClass_FullName(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	class, _ := NewClass(mockClock, 9, "A", 1, nil)

	expected := "9A"
	if class.FullName() != expected {
		t.Errorf("expected FullName = %s, got %s", expected, class.FullName())
	}
}

func TestClass_Setters(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	class, _ := NewClass(mockClock, 9, "A", 1, nil)

	mockClock.Advance(1 * time.Hour)
	class.SetGrade(mockClock, 10)
	if class.Grade() != 10 {
		t.Errorf("expected Grade = 10, got %d", class.Grade())
	}

	class.SetLetter(mockClock, "B")
	if class.Letter() != "B" {
		t.Errorf("expected Letter = B, got %s", class.Letter())
	}

	class.SetAcademicYearID(mockClock, 2)
	if class.AcademicYearID() != 2 {
		t.Errorf("expected AcademicYearID = 2, got %d", class.AcademicYearID())
	}

	teacherID := 5
	class.SetClassTeacherID(mockClock, &teacherID)
	if *class.ClassTeacherID() != teacherID {
		t.Errorf("expected ClassTeacherID = %d, got %d", teacherID, *class.ClassTeacherID())
	}
}

func TestClass_MarkAsDeleted(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	class, _ := NewClass(mockClock, 9, "A", 1, nil)

	if class.IsDeleted() {
		t.Error("expected IsDeleted = false before deletion")
	}

	mockClock.Advance(1 * time.Hour)
	class.MarkAsDeleted(mockClock)

	if !class.IsDeleted() {
		t.Error("expected IsDeleted = true after deletion")
	}
	if class.DeletedAt() == nil {
		t.Fatal("expected non-nil DeletedAt")
	}
}
