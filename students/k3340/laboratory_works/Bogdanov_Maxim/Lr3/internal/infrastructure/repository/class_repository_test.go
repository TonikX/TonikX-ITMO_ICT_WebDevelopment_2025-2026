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

func TestClassRepository_Create(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewClassRepository(db, clock)

	class, err := domain.NewClass(clock, 10, "A", 1, nil)
	if err != nil {
		t.Fatalf("failed to create class: %v", err)
	}

	mock.ExpectQuery(`INSERT INTO classes`).
		WithArgs(10, "A", 1, nil, clock.Now(), clock.Now()).
		WillReturnRows(sqlmock.NewRows([]string{"id"}).AddRow(1))

	ctx := context.Background()
	err = repo.Create(ctx, class)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if class.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", class.ID())
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestClassRepository_GetByID(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewClassRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "grade", "letter", "academic_year_id", "class_teacher_id", "created_at", "updated_at", "deleted_at"}).
		AddRow(1, 10, "A", 1, nil, createdAt, updatedAt, nil)

	mock.ExpectQuery(`SELECT`).
		WithArgs(1).
		WillReturnRows(rows)

	ctx := context.Background()
	class, err := repo.GetByID(ctx, 1)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if class == nil {
		t.Fatal("expected non-nil class")
	}

	if class.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", class.ID())
	}
	if class.Grade() != 10 {
		t.Errorf("expected Grade = 10, got %d", class.Grade())
	}
	if class.Letter() != "A" {
		t.Errorf("expected Letter = A, got %s", class.Letter())
	}
	if class.AcademicYearID() != 1 {
		t.Errorf("expected AcademicYearID = 1, got %d", class.AcademicYearID())
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestClassRepository_GetByID_NotFound(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewClassRepository(db, clock)

	mock.ExpectQuery(`SELECT`).
		WithArgs(999).
		WillReturnError(sql.ErrNoRows)

	ctx := context.Background()
	class, err := repo.GetByID(ctx, 999)
	if err == nil {
		t.Error("expected error, got nil")
	}
	if class != nil {
		t.Errorf("expected nil class, got %v", class)
	}

	var domainErr *domain.Error
	if !errors.As(err, &domainErr) {
		t.Errorf("expected domain.Error, got %T", err)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestClassRepository_GetByIDActive(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewClassRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "grade", "letter", "academic_year_id", "class_teacher_id", "created_at", "updated_at", "deleted_at"}).
		AddRow(1, 10, "A", 1, nil, createdAt, updatedAt, nil)

	mock.ExpectQuery(`SELECT`).
		WithArgs(1).
		WillReturnRows(rows)

	ctx := context.Background()
	class, err := repo.GetByIDActive(ctx, 1)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if class == nil {
		t.Fatal("expected non-nil class")
	}

	if class.IsDeleted() {
		t.Error("expected class to be active")
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestClassRepository_Update(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewClassRepository(db, clock)

	class := domain.RestoreClassFromDB(1, 10, "A", 1, nil, clock.Now(), clock.Now(), nil)
	clock.Advance(1 * time.Hour)
	class.SetGrade(clock, 11)

	mock.ExpectExec(`UPDATE classes`).
		WithArgs(11, "A", 1, nil, class.UpdatedAt(), 1).
		WillReturnResult(sqlmock.NewResult(0, 1))

	ctx := context.Background()
	err = repo.Update(ctx, class)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestClassRepository_Update_NotFound(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewClassRepository(db, clock)

	class := domain.RestoreClassFromDB(999, 10, "A", 1, nil, clock.Now(), clock.Now(), nil)

	mock.ExpectExec(`UPDATE classes`).
		WithArgs(10, "A", 1, nil, class.UpdatedAt(), 999).
		WillReturnResult(sqlmock.NewResult(0, 0))

	ctx := context.Background()
	err = repo.Update(ctx, class)
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

func TestClassRepository_Delete(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewClassRepository(db, clock)

	now := clock.Now()
	mock.ExpectExec(`UPDATE classes`).
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

func TestClassRepository_ListByAcademicYearID(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewClassRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "grade", "letter", "academic_year_id", "class_teacher_id", "created_at", "updated_at", "deleted_at"}).
		AddRow(1, 10, "A", 1, nil, createdAt, updatedAt, nil).
		AddRow(2, 10, "B", 1, nil, createdAt, updatedAt, nil)

	mock.ExpectQuery(`SELECT`).
		WithArgs(1).
		WillReturnRows(rows)

	ctx := context.Background()
	classes, err := repo.ListByAcademicYearID(ctx, 1)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if len(classes) != 2 {
		t.Errorf("expected 2 classes, got %d", len(classes))
	}

	for _, class := range classes {
		if class.AcademicYearID() != 1 {
			t.Errorf("expected AcademicYearID = 1, got %d", class.AcademicYearID())
		}
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}
