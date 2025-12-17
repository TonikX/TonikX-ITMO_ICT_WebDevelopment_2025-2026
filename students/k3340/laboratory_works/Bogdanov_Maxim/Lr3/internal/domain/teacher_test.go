package domain

import (
	"testing"
	"time"

	mockclock "school-service/internal/infrastructure/clock"
)

func TestNewTeacher(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))

	tests := []struct {
		name        string
		firstName   string
		lastName    string
		middleName  *string
		classroomID *int
		wantErr     bool
	}{
		{
			name:        "valid teacher",
			firstName:   "John",
			lastName:    "Doe",
			middleName:  nil,
			classroomID: nil,
			wantErr:     false,
		},
		{
			name:        "valid teacher with middle name",
			firstName:   "John",
			lastName:    "Doe",
			middleName:  stringPtr("Middle"),
			classroomID: intPtr(1),
			wantErr:     false,
		},
		{
			name:        "empty first name",
			firstName:   "",
			lastName:    "Doe",
			middleName:  nil,
			classroomID: nil,
			wantErr:     true,
		},
		{
			name:        "empty last name",
			firstName:   "John",
			lastName:    "",
			middleName:  nil,
			classroomID: nil,
			wantErr:     true,
		},
		{
			name:        "first name too long",
			firstName:   stringWithLength(51),
			lastName:    "Doe",
			middleName:  nil,
			classroomID: nil,
			wantErr:     true,
		},
		{
			name:        "last name too long",
			firstName:   "John",
			lastName:    stringWithLength(51),
			middleName:  nil,
			classroomID: nil,
			wantErr:     true,
		},
		{
			name:        "middle name too long",
			firstName:   "John",
			lastName:    "Doe",
			middleName:  stringPtr(stringWithLength(51)),
			classroomID: nil,
			wantErr:     true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			teacher, err := NewTeacher(mockClock, tt.firstName, tt.lastName, tt.middleName, tt.classroomID)
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
				if teacher != nil {
					t.Errorf("expected nil teacher, got %v", teacher)
				}
			} else {
				if err != nil {
					t.Errorf("unexpected error: %v", err)
				}
				if teacher == nil {
					t.Fatal("expected non-nil teacher")
				}
				if teacher.FirstName() != tt.firstName {
					t.Errorf("expected FirstName = %s, got %s", tt.firstName, teacher.FirstName())
				}
				if teacher.LastName() != tt.lastName {
					t.Errorf("expected LastName = %s, got %s", tt.lastName, teacher.LastName())
				}
				if !timeEqual(teacher.CreatedAt(), teacher.UpdatedAt()) {
					t.Errorf("expected CreatedAt = UpdatedAt")
				}
			}
		})
	}
}

func TestRestoreTeacherFromDB(t *testing.T) {
	now := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	middleName := "Middle"
	classroomID := 1

	teacher := RestoreTeacherFromDB(1, "John", "Doe", &middleName, &classroomID, now, now, nil)

	if teacher.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", teacher.ID())
	}
	if teacher.FirstName() != "John" {
		t.Errorf("expected FirstName = John, got %s", teacher.FirstName())
	}
	if teacher.LastName() != "Doe" {
		t.Errorf("expected LastName = Doe, got %s", teacher.LastName())
	}
	if *teacher.MiddleName() != middleName {
		t.Errorf("expected MiddleName = %s, got %s", middleName, *teacher.MiddleName())
	}
	if *teacher.ClassroomID() != classroomID {
		t.Errorf("expected ClassroomID = %d, got %d", classroomID, *teacher.ClassroomID())
	}
	if teacher.CreatedAt() != now {
		t.Errorf("expected CreatedAt = %v, got %v", now, teacher.CreatedAt())
	}
	if teacher.IsDeleted() {
		t.Error("expected IsDeleted = false")
	}
}

func TestTeacher_Setters(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	teacher, _ := NewTeacher(mockClock, "John", "Doe", nil, nil)

	mockClock.Advance(1 * time.Hour)
	teacher.SetFirstName(mockClock, "Jane")
	if teacher.FirstName() != "Jane" {
		t.Errorf("expected FirstName = Jane, got %s", teacher.FirstName())
	}
	if !timeEqual(teacher.UpdatedAt(), mockClock.Now()) {
		t.Errorf("expected UpdatedAt to be updated")
	}

	mockClock.Advance(1 * time.Hour)
	teacher.SetLastName(mockClock, "Smith")
	if teacher.LastName() != "Smith" {
		t.Errorf("expected LastName = Smith, got %s", teacher.LastName())
	}

	middleName := "Middle"
	teacher.SetMiddleName(mockClock, &middleName)
	if *teacher.MiddleName() != middleName {
		t.Errorf("expected MiddleName = %s, got %s", middleName, *teacher.MiddleName())
	}

	classroomID := 5
	teacher.SetClassroomID(mockClock, &classroomID)
	if *teacher.ClassroomID() != classroomID {
		t.Errorf("expected ClassroomID = %d, got %d", classroomID, *teacher.ClassroomID())
	}
}

func TestTeacher_MarkAsDeleted(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	teacher, _ := NewTeacher(mockClock, "John", "Doe", nil, nil)

	if teacher.IsDeleted() {
		t.Error("expected IsDeleted = false before deletion")
	}

	mockClock.Advance(1 * time.Hour)
	deletedAt := mockClock.Now()
	teacher.MarkAsDeleted(mockClock)

	if !teacher.IsDeleted() {
		t.Error("expected IsDeleted = true after deletion")
	}
	if teacher.DeletedAt() == nil {
		t.Fatal("expected non-nil DeletedAt")
	}
	if !timeEqual(*teacher.DeletedAt(), deletedAt) {
		t.Errorf("expected DeletedAt = %v, got %v", deletedAt, *teacher.DeletedAt())
	}
	if !timeEqual(teacher.UpdatedAt(), deletedAt) {
		t.Errorf("expected UpdatedAt = DeletedAt")
	}
}

func TestTeacher_Validate(t *testing.T) {
	tests := []struct {
		name    string
		teacher *Teacher
		wantErr bool
	}{
		{
			name: "valid teacher",
			teacher: &Teacher{
				firstName: "John",
				lastName:  "Doe",
			},
			wantErr: false,
		},
		{
			name: "empty first name",
			teacher: &Teacher{
				firstName: "",
				lastName:  "Doe",
			},
			wantErr: true,
		},
		{
			name: "empty last name",
			teacher: &Teacher{
				firstName: "John",
				lastName:  "",
			},
			wantErr: true,
		},
		{
			name: "first name too long",
			teacher: &Teacher{
				firstName: stringWithLength(51),
				lastName:  "Doe",
			},
			wantErr: true,
		},
		{
			name: "last name too long",
			teacher: &Teacher{
				firstName: "John",
				lastName:  stringWithLength(51),
			},
			wantErr: true,
		},
		{
			name: "middle name too long",
			teacher: &Teacher{
				firstName:  "John",
				lastName:   "Doe",
				middleName: stringPtr(stringWithLength(51)),
			},
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tt.teacher.Validate()
			if tt.wantErr {
				if err == nil {
					t.Errorf("expected error, got nil")
				}
			} else {
				if err != nil {
					t.Errorf("unexpected error: %v", err)
				}
			}
		})
	}
}

func stringPtr(s string) *string {
	return &s
}

func intPtr(i int) *int {
	return &i
}

func stringWithLength(n int) string {
	result := ""
	for i := 0; i < n; i++ {
		result += "a"
	}
	return result
}

func timeEqual(t1, t2 time.Time) bool {
	return t1.Equal(t2)
}
