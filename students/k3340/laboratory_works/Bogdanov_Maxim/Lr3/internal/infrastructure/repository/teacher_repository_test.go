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

func TestTeacherRepository_Create(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewTeacherRepository(db, clock)

	teacher, err := domain.NewTeacher(clock, "John", "Doe", nil, nil)
	if err != nil {
		t.Fatalf("failed to create teacher: %v", err)
	}

	mock.ExpectQuery(`INSERT INTO teachers`).
		WithArgs("John", "Doe", nil, nil, clock.Now(), clock.Now()).
		WillReturnRows(sqlmock.NewRows([]string{"id"}).AddRow(1))

	ctx := context.Background()
	err = repo.Create(ctx, teacher)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if teacher.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", teacher.ID())
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestTeacherRepository_Create_WithOptionalFields(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewTeacherRepository(db, clock)

	middleName := "Middle"
	classroomID := 5
	teacher, err := domain.NewTeacher(clock, "John", "Doe", &middleName, &classroomID)
	if err != nil {
		t.Fatalf("failed to create teacher: %v", err)
	}

	mock.ExpectQuery(`INSERT INTO teachers`).
		WithArgs("John", "Doe", &middleName, &classroomID, clock.Now(), clock.Now()).
		WillReturnRows(sqlmock.NewRows([]string{"id"}).AddRow(1))

	ctx := context.Background()
	err = repo.Create(ctx, teacher)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if teacher.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", teacher.ID())
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestTeacherRepository_Create_DatabaseError(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewTeacherRepository(db, clock)

	teacher, err := domain.NewTeacher(clock, "John", "Doe", nil, nil)
	if err != nil {
		t.Fatalf("failed to create teacher: %v", err)
	}

	mock.ExpectQuery(`INSERT INTO teachers`).
		WillReturnError(errors.New("database error"))

	ctx := context.Background()
	err = repo.Create(ctx, teacher)
	if err == nil {
		t.Error("expected error, got nil")
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestTeacherRepository_GetByID(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewTeacherRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "first_name", "last_name", "middle_name", "classroom_id", "created_at", "updated_at", "deleted_at"}).
		AddRow(1, "John", "Doe", nil, nil, createdAt, updatedAt, nil)

	mock.ExpectQuery(`SELECT`).
		WithArgs(1).
		WillReturnRows(rows)

	ctx := context.Background()
	teacher, err := repo.GetByID(ctx, 1)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if teacher == nil {
		t.Fatal("expected non-nil teacher")
	}

	if teacher.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", teacher.ID())
	}
	if teacher.FirstName() != "John" {
		t.Errorf("expected FirstName = John, got %s", teacher.FirstName())
	}
	if teacher.LastName() != "Doe" {
		t.Errorf("expected LastName = Doe, got %s", teacher.LastName())
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestTeacherRepository_GetByID_NotFound(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewTeacherRepository(db, clock)

	mock.ExpectQuery(`SELECT`).
		WithArgs(999).
		WillReturnError(sql.ErrNoRows)

	ctx := context.Background()
	teacher, err := repo.GetByID(ctx, 999)
	if err == nil {
		t.Error("expected error, got nil")
	}
	if teacher != nil {
		t.Errorf("expected nil teacher, got %v", teacher)
	}

	var domainErr *domain.Error
	if !errors.As(err, &domainErr) {
		t.Errorf("expected domain.Error, got %T", err)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestTeacherRepository_GetByIDActive(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewTeacherRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "first_name", "last_name", "middle_name", "classroom_id", "created_at", "updated_at", "deleted_at"}).
		AddRow(1, "John", "Doe", nil, nil, createdAt, updatedAt, nil)

	mock.ExpectQuery(`SELECT`).
		WithArgs(1).
		WillReturnRows(rows)

	ctx := context.Background()
	teacher, err := repo.GetByIDActive(ctx, 1)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if teacher == nil {
		t.Fatal("expected non-nil teacher")
	}

	if teacher.IsDeleted() {
		t.Error("expected teacher to be active")
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestTeacherRepository_Update(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewTeacherRepository(db, clock)

	teacher := domain.RestoreTeacherFromDB(1, "John", "Doe", nil, nil, clock.Now(), clock.Now(), nil)
	clock.Advance(1 * time.Hour)
	teacher.SetFirstName(clock, "Jane")

	mock.ExpectExec(`UPDATE teachers`).
		WithArgs("Jane", "Doe", nil, nil, teacher.UpdatedAt(), 1).
		WillReturnResult(sqlmock.NewResult(0, 1))

	ctx := context.Background()
	err = repo.Update(ctx, teacher)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestTeacherRepository_Update_NotFound(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewTeacherRepository(db, clock)

	teacher := domain.RestoreTeacherFromDB(999, "John", "Doe", nil, nil, clock.Now(), clock.Now(), nil)

	mock.ExpectExec(`UPDATE teachers`).
		WithArgs("John", "Doe", nil, nil, teacher.UpdatedAt(), 999).
		WillReturnResult(sqlmock.NewResult(0, 0))

	ctx := context.Background()
	err = repo.Update(ctx, teacher)
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

func TestTeacherRepository_Delete(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewTeacherRepository(db, clock)

	now := clock.Now()
	mock.ExpectExec(`UPDATE teachers`).
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

func TestTeacherRepository_Delete_NotFound(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewTeacherRepository(db, clock)

	now := clock.Now()
	mock.ExpectExec(`UPDATE teachers`).
		WithArgs(now, now, 999).
		WillReturnResult(sqlmock.NewResult(0, 0))

	ctx := context.Background()
	err = repo.Delete(ctx, 999)
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

func TestTeacherRepository_List(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewTeacherRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	deletedAt := time.Date(2024, 1, 2, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "first_name", "last_name", "middle_name", "classroom_id", "created_at", "updated_at", "deleted_at"}).
		AddRow(1, "John", "Doe", nil, nil, createdAt, updatedAt, nil).
		AddRow(2, "Jane", "Smith", sql.NullString{String: "Middle", Valid: true}, sql.NullInt64{Int64: 5, Valid: true}, createdAt, updatedAt, deletedAt)

	mock.ExpectQuery(`SELECT`).
		WillReturnRows(rows)

	ctx := context.Background()
	teachers, err := repo.List(ctx)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if len(teachers) != 2 {
		t.Errorf("expected 2 teachers, got %d", len(teachers))
	}

	if teachers[0].ID() != 1 {
		t.Errorf("expected first teacher ID = 1, got %d", teachers[0].ID())
	}
	if teachers[1].ID() != 2 {
		t.Errorf("expected second teacher ID = 2, got %d", teachers[1].ID())
	}

	if !teachers[1].IsDeleted() {
		t.Error("expected second teacher to be deleted")
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestTeacherRepository_ListActive(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewTeacherRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "first_name", "last_name", "middle_name", "classroom_id", "created_at", "updated_at", "deleted_at"}).
		AddRow(1, "John", "Doe", nil, nil, createdAt, updatedAt, nil).
		AddRow(2, "Jane", "Smith", nil, nil, createdAt, updatedAt, nil)

	mock.ExpectQuery(`SELECT`).
		WillReturnRows(rows)

	ctx := context.Background()
	teachers, err := repo.ListActive(ctx)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if len(teachers) != 2 {
		t.Errorf("expected 2 teachers, got %d", len(teachers))
	}

	for _, teacher := range teachers {
		if teacher.IsDeleted() {
			t.Errorf("expected teacher %d to be active", teacher.ID())
		}
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}
