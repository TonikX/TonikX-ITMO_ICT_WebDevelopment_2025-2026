package domain

import (
	"errors"
	"testing"
)

func TestNewValidationError(t *testing.T) {
	err := NewValidationError("teacher", "name", "John", "name is too short")

	if err.Code != ErrorCodeValidation {
		t.Errorf("expected Code = %s, got %s", ErrorCodeValidation, err.Code)
	}
	if !errors.Is(err.BaseErr, ErrValidation) {
		t.Errorf("expected BaseErr = %v, got %v", ErrValidation, err.BaseErr)
	}
	if err.Entity != "teacher" {
		t.Errorf("expected Entity = teacher, got %s", err.Entity)
	}
	if err.Field != "name" {
		t.Errorf("expected Field = name, got %s", err.Field)
	}
	if err.Value != "John" {
		t.Errorf("expected Value = John, got %v", err.Value)
	}
	if err.Reason != "name is too short" {
		t.Errorf("expected Reason = name is too short, got %s", err.Reason)
	}
}

func TestNewNotFoundError(t *testing.T) {
	err := NewNotFoundError("student", "id", 123, "student not found")

	if err.Code != ErrorCodeNotFound {
		t.Errorf("expected Code = %s, got %s", ErrorCodeNotFound, err.Code)
	}
	if !errors.Is(err.BaseErr, ErrNotFound) {
		t.Errorf("expected BaseErr = %v, got %v", ErrNotFound, err.BaseErr)
	}
	if err.Entity != "student" {
		t.Errorf("expected Entity = student, got %s", err.Entity)
	}
	if err.Field != "id" {
		t.Errorf("expected Field = id, got %s", err.Field)
	}
	if err.Value != 123 {
		t.Errorf("expected Value = 123, got %v", err.Value)
	}
	if err.Reason != "student not found" {
		t.Errorf("expected Reason = student not found, got %s", err.Reason)
	}
}

func TestNewAlreadyExistsError(t *testing.T) {
	err := NewAlreadyExistsError("class", "name", "10A", "class already exists")

	if err.Code != ErrorCodeAlreadyExists {
		t.Errorf("expected Code = %s, got %s", ErrorCodeAlreadyExists, err.Code)
	}
	if !errors.Is(err.BaseErr, ErrAlreadyExists) {
		t.Errorf("expected BaseErr = %v, got %v", ErrAlreadyExists, err.BaseErr)
	}
	if err.Entity != "class" {
		t.Errorf("expected Entity = class, got %s", err.Entity)
	}
	if err.Field != "name" {
		t.Errorf("expected Field = name, got %s", err.Field)
	}
	if err.Value != "10A" {
		t.Errorf("expected Value = 10A, got %v", err.Value)
	}
	if err.Reason != "class already exists" {
		t.Errorf("expected Reason = class already exists, got %s", err.Reason)
	}
}

func TestNewDeletedError(t *testing.T) {
	err := NewDeletedError("teacher", "id", 456, "teacher is deleted")

	if err.Code != ErrorCodeDeleted {
		t.Errorf("expected Code = %s, got %s", ErrorCodeDeleted, err.Code)
	}
	if !errors.Is(err.BaseErr, ErrDeleted) {
		t.Errorf("expected BaseErr = %v, got %v", ErrDeleted, err.BaseErr)
	}
	if err.Entity != "teacher" {
		t.Errorf("expected Entity = teacher, got %s", err.Entity)
	}
	if err.Field != "id" {
		t.Errorf("expected Field = id, got %s", err.Field)
	}
	if err.Value != 456 {
		t.Errorf("expected Value = 456, got %v", err.Value)
	}
	if err.Reason != "teacher is deleted" {
		t.Errorf("expected Reason = teacher is deleted, got %s", err.Reason)
	}
}

func TestError_Error(t *testing.T) {
	tests := []struct {
		name     string
		err      *Error
		contains []string
	}{
		{
			name: "with entity and field",
			err: &Error{
				BaseErr: ErrValidation,
				Entity:  "teacher",
				Field:   "name",
				Value:   "John",
				Reason:  "too short",
			},
			contains: []string{"validation error", "entity=teacher", "field=name", "too short", "value=John"},
		},
		{
			name: "with entity only",
			err: &Error{
				BaseErr: ErrNotFound,
				Entity:  "student",
				Reason:  "not found",
			},
			contains: []string{"resource not found", "entity=student", "not found"},
		},
		{
			name: "with field only",
			err: &Error{
				BaseErr: ErrValidation,
				Field:   "email",
				Value:   "invalid",
				Reason:  "invalid format",
			},
			contains: []string{"validation error", "field=email", "invalid format", "value=invalid"},
		},
		{
			name: "with reason only",
			err: &Error{
				BaseErr: ErrValidation,
				Reason:  "invalid data",
			},
			contains: []string{"validation error", "invalid data"},
		},
		{
			name: "with nil BaseErr",
			err: &Error{
				Entity: "teacher",
				Reason: "error occurred",
			},
			contains: []string{"domain error", "entity=teacher", "error occurred"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			errStr := tt.err.Error()
			for _, substr := range tt.contains {
				if !contains(errStr, substr) {
					t.Errorf("expected error string to contain '%s', got: %s", substr, errStr)
				}
			}
		})
	}
}

func TestError_Unwrap(t *testing.T) {
	err := NewValidationError("teacher", "name", "John", "too short")
	baseErr := err.Unwrap()

	if baseErr != ErrValidation {
		t.Errorf("expected Unwrap() = %v, got %v", ErrValidation, baseErr)
	}
}

func TestError_Unwrap_NilBaseErr(t *testing.T) {
	err := &Error{
		Code:   ErrorCodeValidation,
		Entity: "teacher",
		Reason: "error",
	}
	baseErr := err.Unwrap()

	if baseErr != nil {
		t.Errorf("expected Unwrap() = nil, got %v", baseErr)
	}
}

func TestError_Is(t *testing.T) {
	err := NewValidationError("teacher", "name", "John", "too short")

	if !errors.Is(err, ErrValidation) {
		t.Errorf("expected errors.Is(err, ErrValidation) = true, got false")
	}

	if errors.Is(err, ErrNotFound) {
		t.Errorf("expected errors.Is(err, ErrNotFound) = false, got true")
	}
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(substr) == 0 || len(s) > len(substr) && (s[:len(substr)] == substr || s[len(s)-len(substr):] == substr || containsMiddle(s, substr)))
}

func containsMiddle(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}
