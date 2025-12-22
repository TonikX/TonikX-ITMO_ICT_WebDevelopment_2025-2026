package domain

import (
	"testing"
	"time"

	mockclock "school-service/internal/infrastructure/clock"
)

func TestNewStudent(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))

	tests := []struct {
		name       string
		firstName  string
		lastName   string
		middleName *string
		genderID   int
		classID    int
		wantErr    bool
	}{
		{
			name:       "valid student",
			firstName:  "John",
			lastName:   "Doe",
			middleName: nil,
			genderID:   1,
			classID:    1,
			wantErr:    false,
		},
		{
			name:       "valid student with middle name",
			firstName:  "John",
			lastName:   "Doe",
			middleName: stringPtr("Middle"),
			genderID:   1,
			classID:    1,
			wantErr:    false,
		},
		{
			name:       "empty first name",
			firstName:  "",
			lastName:   "Doe",
			middleName: nil,
			genderID:   1,
			classID:    1,
			wantErr:    true,
		},
		{
			name:       "empty last name",
			firstName:  "John",
			lastName:   "",
			middleName: nil,
			genderID:   1,
			classID:    1,
			wantErr:    true,
		},
		{
			name:       "invalid genderID",
			firstName:  "John",
			lastName:   "Doe",
			middleName: nil,
			genderID:   0,
			classID:    1,
			wantErr:    true,
		},
		{
			name:       "invalid classID",
			firstName:  "John",
			lastName:   "Doe",
			middleName: nil,
			genderID:   1,
			classID:    0,
			wantErr:    true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			student, err := NewStudent(mockClock, tt.firstName, tt.lastName, tt.middleName, tt.genderID, tt.classID)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				if student != nil {
					t.Errorf("expected nil student, got %v", student)
				}
			} else {
				if err != nil {
					t.Errorf("unexpected error: %v", err)
				}
				if student == nil {
					t.Fatal("expected non-nil student")
				}
				if student.FirstName() != tt.firstName {
					t.Errorf("expected FirstName = %s, got %s", tt.firstName, student.FirstName())
				}
				if student.GenderID() != tt.genderID {
					t.Errorf("expected GenderID = %d, got %d", tt.genderID, student.GenderID())
				}
				if student.ClassID() != tt.classID {
					t.Errorf("expected ClassID = %d, got %d", tt.classID, student.ClassID())
				}
			}
		})
	}
}

func TestRestoreStudentFromDB(t *testing.T) {
	now := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	middleName := "Middle"

	student := RestoreStudentFromDB(1, "John", "Doe", &middleName, 1, 2, now, now, nil)

	if student.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", student.ID())
	}
	if student.FirstName() != "John" {
		t.Errorf("expected FirstName = John, got %s", student.FirstName())
	}
	if student.GenderID() != 1 {
		t.Errorf("expected GenderID = 1, got %d", student.GenderID())
	}
	if student.ClassID() != 2 {
		t.Errorf("expected ClassID = 2, got %d", student.ClassID())
	}
	if !timeEqual(student.CreatedAt(), now) {
		t.Errorf("expected CreatedAt = %v, got %v", now, student.CreatedAt())
	}
	if student.IsDeleted() {
		t.Error("expected IsDeleted = false")
	}
}

func TestStudent_Setters(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	student, _ := NewStudent(mockClock, "John", "Doe", nil, 1, 1)

	mockClock.Advance(1 * time.Hour)
	student.SetFirstName(mockClock, "Jane")
	if student.FirstName() != "Jane" {
		t.Errorf("expected FirstName = Jane, got %s", student.FirstName())
	}

	student.SetGenderID(mockClock, 2)
	if student.GenderID() != 2 {
		t.Errorf("expected GenderID = 2, got %d", student.GenderID())
	}

	student.SetClassID(mockClock, 3)
	if student.ClassID() != 3 {
		t.Errorf("expected ClassID = 3, got %d", student.ClassID())
	}
}

func TestStudent_MarkAsDeleted(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	student, _ := NewStudent(mockClock, "John", "Doe", nil, 1, 1)

	if student.IsDeleted() {
		t.Error("expected IsDeleted = false before deletion")
	}

	mockClock.Advance(1 * time.Hour)
	student.MarkAsDeleted(mockClock)

	if !student.IsDeleted() {
		t.Error("expected IsDeleted = true after deletion")
	}
	if student.DeletedAt() == nil {
		t.Fatal("expected non-nil DeletedAt")
	}
}
