package repository

import (
	"context"
	"database/sql"
	"errors"
	"testing"
	"time"

	"github.com/DATA-DOG/go-sqlmock"
	"school-service/internal/domain"
	mockclock "school-service/internal/infrastructure/clock"
)

func TestStudentRepository_Create(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewStudentRepository(db, clock)

	student, err := domain.NewStudent(clock, "John", "Doe", nil, 1, 1)
	if err != nil {
		t.Fatalf("failed to create student: %v", err)
	}

	mock.ExpectQuery(`INSERT INTO students`).
		WithArgs("John", "Doe", nil, 1, 1, clock.Now(), clock.Now()).
		WillReturnRows(sqlmock.NewRows([]string{"id"}).AddRow(1))

	ctx := context.Background()
	err = repo.Create(ctx, student)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if student.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", student.ID())
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestStudentRepository_GetByID(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewStudentRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "first_name", "last_name", "middle_name", "gender_id", "class_id", "created_at", "updated_at", "deleted_at"}).
		AddRow(1, "John", "Doe", nil, 1, 1, createdAt, updatedAt, nil)

	mock.ExpectQuery(`SELECT`).
		WithArgs(1).
		WillReturnRows(rows)

	ctx := context.Background()
	student, err := repo.GetByID(ctx, 1)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if student == nil {
		t.Fatal("expected non-nil student")
	}

	if student.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", student.ID())
	}
	if student.FirstName() != "John" {
		t.Errorf("expected FirstName = John, got %s", student.FirstName())
	}
	if student.GenderID() != 1 {
		t.Errorf("expected GenderID = 1, got %d", student.GenderID())
	}
	if student.ClassID() != 1 {
		t.Errorf("expected ClassID = 1, got %d", student.ClassID())
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestStudentRepository_GetByID_NotFound(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewStudentRepository(db, clock)

	mock.ExpectQuery(`SELECT`).
		WithArgs(999).
		WillReturnError(sql.ErrNoRows)

	ctx := context.Background()
	student, err := repo.GetByID(ctx, 999)
	if err == nil {
		t.Error("expected error, got nil")
	}
	if student != nil {
		t.Errorf("expected nil student, got %v", student)
	}

	var domainErr *domain.Error
	if !errors.As(err, &domainErr) {
		t.Errorf("expected domain.Error, got %T", err)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestStudentRepository_GetByIDActive(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewStudentRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "first_name", "last_name", "middle_name", "gender_id", "class_id", "created_at", "updated_at", "deleted_at"}).
		AddRow(1, "John", "Doe", nil, 1, 1, createdAt, updatedAt, nil)

	mock.ExpectQuery(`SELECT`).
		WithArgs(1).
		WillReturnRows(rows)

	ctx := context.Background()
	student, err := repo.GetByIDActive(ctx, 1)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if student == nil {
		t.Fatal("expected non-nil student")
	}

	if student.IsDeleted() {
		t.Error("expected student to be active")
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestStudentRepository_Update(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewStudentRepository(db, clock)

	student := domain.RestoreStudentFromDB(1, "John", "Doe", nil, 1, 1, clock.Now(), clock.Now(), nil)
	clock.Advance(1 * time.Hour)
	student.SetFirstName(clock, "Jane")

	mock.ExpectExec(`UPDATE students`).
		WithArgs("Jane", "Doe", nil, 1, 1, student.UpdatedAt(), 1).
		WillReturnResult(sqlmock.NewResult(0, 1))

	ctx := context.Background()
	err = repo.Update(ctx, student)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestStudentRepository_Update_NotFound(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewStudentRepository(db, clock)

	student := domain.RestoreStudentFromDB(999, "John", "Doe", nil, 1, 1, clock.Now(), clock.Now(), nil)

	mock.ExpectExec(`UPDATE students`).
		WithArgs("John", "Doe", nil, 1, 1, student.UpdatedAt(), 999).
		WillReturnResult(sqlmock.NewResult(0, 0))

	ctx := context.Background()
	err = repo.Update(ctx, student)
	if err == nil {
		t.Error("expected error, got nil")
	}

	var domainErr *domain.Error
	if !errors.As(err, &domainErr) {
		t.Errorf("expected domain.Error, got %T", err)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestStudentRepository_Delete(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewStudentRepository(db, clock)

	now := clock.Now()
	mock.ExpectExec(`UPDATE students`).
		WithArgs(now, now, 1).
		WillReturnResult(sqlmock.NewResult(0, 1))

	ctx := context.Background()
	err = repo.Delete(ctx, 1)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestStudentRepository_ListByClassID(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewStudentRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "first_name", "last_name", "middle_name", "gender_id", "class_id", "created_at", "updated_at", "deleted_at"}).
		AddRow(1, "John", "Doe", nil, 1, 5, createdAt, updatedAt, nil).
		AddRow(2, "Jane", "Smith", nil, 2, 5, createdAt, updatedAt, nil)

	mock.ExpectQuery(`SELECT`).
		WithArgs(5).
		WillReturnRows(rows)

	ctx := context.Background()
	students, err := repo.ListByClassID(ctx, 5)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if len(students) != 2 {
		t.Errorf("expected 2 students, got %d", len(students))
	}

	for _, student := range students {
		if student.ClassID() != 5 {
			t.Errorf("expected ClassID = 5, got %d", student.ClassID())
		}
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestStudentRepository_ListActiveByClassID(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewStudentRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "first_name", "last_name", "middle_name", "gender_id", "class_id", "created_at", "updated_at", "deleted_at"}).
		AddRow(1, "John", "Doe", nil, 1, 5, createdAt, updatedAt, nil).
		AddRow(2, "Jane", "Smith", nil, 2, 5, createdAt, updatedAt, nil)

	mock.ExpectQuery(`SELECT`).
		WithArgs(5).
		WillReturnRows(rows)

	ctx := context.Background()
	students, err := repo.ListActiveByClassID(ctx, 5)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if len(students) != 2 {
		t.Errorf("expected 2 students, got %d", len(students))
	}

	for _, student := range students {
		if student.ClassID() != 5 {
			t.Errorf("expected ClassID = 5, got %d", student.ClassID())
		}
		if student.IsDeleted() {
			t.Errorf("expected student %d to be active", student.ID())
		}
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}
