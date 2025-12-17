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

func TestGradeRepository_Create(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewGradeRepository(db, clock)

	grade, err := domain.NewGrade(clock, 1, 1, 1, 5)
	if err != nil {
		t.Fatalf("failed to create grade: %v", err)
	}

	mock.ExpectQuery(`INSERT INTO grades`).
		WithArgs(1, 1, 1, 5, clock.Now(), clock.Now()).
		WillReturnRows(sqlmock.NewRows([]string{"id"}).AddRow(1))

	ctx := context.Background()
	err = repo.Create(ctx, grade)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if grade.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", grade.ID())
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestGradeRepository_GetByID(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewGradeRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "student_id", "subject_id", "grading_period_id", "grade", "created_at", "updated_at"}).
		AddRow(1, 1, 1, 1, 5, createdAt, updatedAt)

	mock.ExpectQuery(`SELECT`).
		WithArgs(1).
		WillReturnRows(rows)

	ctx := context.Background()
	grade, err := repo.GetByID(ctx, 1)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if grade == nil {
		t.Fatal("expected non-nil grade")
	}

	if grade.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", grade.ID())
	}

	if grade.Grade() != 5 {
		t.Errorf("expected Grade = 5, got %d", grade.Grade())
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestGradeRepository_GetByID_NotFound(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewGradeRepository(db, clock)

	mock.ExpectQuery(`SELECT`).
		WithArgs(999).
		WillReturnError(sql.ErrNoRows)

	ctx := context.Background()
	grade, err := repo.GetByID(ctx, 999)
	if err == nil {
		t.Error("expected error, got nil")
	}

	if grade != nil {
		t.Errorf("expected nil grade, got %v", grade)
	}

	var domainErr *domain.Error
	if !errors.As(err, &domainErr) {
		t.Errorf("expected domain.Error, got %T", err)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestGradeRepository_Update(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewGradeRepository(db, clock)

	grade := domain.RestoreGradeFromDB(1, 1, 1, 1, 4, clock.Now(), clock.Now())
	grade.SetGrade(clock, 5)

	mock.ExpectExec(`UPDATE grades`).
		WithArgs(1, 1, 1, 5, clock.Now(), 1).
		WillReturnResult(sqlmock.NewResult(0, 1))

	ctx := context.Background()
	err = repo.Update(ctx, grade)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestGradeRepository_Delete(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewGradeRepository(db, clock)

	mock.ExpectExec(`DELETE FROM grades`).
		WithArgs(1).
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

func TestGradeRepository_List(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewGradeRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "student_id", "subject_id", "grading_period_id", "grade", "created_at", "updated_at"}).
		AddRow(1, 1, 1, 1, 5, createdAt, updatedAt).
		AddRow(2, 2, 1, 1, 4, createdAt, updatedAt)

	mock.ExpectQuery(`SELECT`).
		WillReturnRows(rows)

	ctx := context.Background()
	grades, err := repo.List(ctx)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if len(grades) != 2 {
		t.Errorf("expected 2 grades, got %d", len(grades))
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestGradeRepository_ListByStudentID(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewGradeRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "student_id", "subject_id", "grading_period_id", "grade", "created_at", "updated_at"}).
		AddRow(1, 1, 1, 1, 5, createdAt, updatedAt)

	mock.ExpectQuery(`SELECT`).
		WithArgs(1).
		WillReturnRows(rows)

	ctx := context.Background()
	grades, err := repo.ListByStudentID(ctx, 1)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if len(grades) != 1 {
		t.Errorf("expected 1 grade, got %d", len(grades))
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestGradeRepository_ListByClassAndSubject(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewGradeRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "student_id", "subject_id", "grading_period_id", "grade", "created_at", "updated_at"}).
		AddRow(1, 1, 1, 1, 5, createdAt, updatedAt)

	mock.ExpectQuery(`SELECT`).
		WithArgs(1, 1).
		WillReturnRows(rows)

	ctx := context.Background()
	grades, err := repo.ListByClassAndSubject(ctx, 1, 1)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if len(grades) != 1 {
		t.Errorf("expected 1 grade, got %d", len(grades))
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}
