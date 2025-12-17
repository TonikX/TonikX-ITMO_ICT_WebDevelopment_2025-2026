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

func TestScheduleRepository_Create(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewScheduleRepository(db, clock)

	schedule, err := domain.NewSchedule(clock, 1, 1, 1, 1, 1, 1)
	if err != nil {
		t.Fatalf("failed to create schedule: %v", err)
	}

	mock.ExpectQuery(`INSERT INTO schedule`).
		WithArgs(1, 1, 1, 1, 1, 1, clock.Now(), clock.Now()).
		WillReturnRows(sqlmock.NewRows([]string{"id"}).AddRow(1))

	ctx := context.Background()
	err = repo.Create(ctx, schedule)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if schedule.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", schedule.ID())
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestScheduleRepository_GetByID(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewScheduleRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "class_id", "weekday_id", "lesson_number", "subject_id", "teacher_id", "classroom_id", "created_at", "updated_at"}).
		AddRow(1, 1, 1, 1, 1, 1, 1, createdAt, updatedAt)

	mock.ExpectQuery(`SELECT`).
		WithArgs(1).
		WillReturnRows(rows)

	ctx := context.Background()
	schedule, err := repo.GetByID(ctx, 1)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if schedule == nil {
		t.Fatal("expected non-nil schedule")
	}

	if schedule.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", schedule.ID())
	}

	if schedule.ClassID() != 1 {
		t.Errorf("expected ClassID = 1, got %d", schedule.ClassID())
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestScheduleRepository_GetByID_NotFound(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewScheduleRepository(db, clock)

	mock.ExpectQuery(`SELECT`).
		WithArgs(999).
		WillReturnError(sql.ErrNoRows)

	ctx := context.Background()
	schedule, err := repo.GetByID(ctx, 999)
	if err == nil {
		t.Error("expected error, got nil")
	}

	if schedule != nil {
		t.Errorf("expected nil schedule, got %v", schedule)
	}

	var domainErr *domain.Error
	if !errors.As(err, &domainErr) {
		t.Errorf("expected domain.Error, got %T", err)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestScheduleRepository_Update(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewScheduleRepository(db, clock)

	schedule := domain.RestoreScheduleFromDB(1, 1, 1, 1, 1, 1, 1, clock.Now(), clock.Now())
	schedule.SetClassID(clock, 2)
	schedule.SetSubjectID(clock, 2)

	mock.ExpectExec(`UPDATE schedule`).
		WithArgs(2, 1, 1, 2, 1, 1, clock.Now(), 1).
		WillReturnResult(sqlmock.NewResult(0, 1))

	ctx := context.Background()
	err = repo.Update(ctx, schedule)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestScheduleRepository_Delete(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewScheduleRepository(db, clock)

	mock.ExpectExec(`DELETE FROM schedule`).
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

func TestScheduleRepository_List(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewScheduleRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "class_id", "weekday_id", "lesson_number", "subject_id", "teacher_id", "classroom_id", "created_at", "updated_at"}).
		AddRow(1, 1, 1, 1, 1, 1, 1, createdAt, updatedAt).
		AddRow(2, 1, 1, 2, 2, 2, 2, createdAt, updatedAt)

	mock.ExpectQuery(`SELECT`).
		WillReturnRows(rows)

	ctx := context.Background()
	schedules, err := repo.List(ctx)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if len(schedules) != 2 {
		t.Errorf("expected 2 schedules, got %d", len(schedules))
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestScheduleRepository_ListByClassID(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewScheduleRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "class_id", "weekday_id", "lesson_number", "subject_id", "teacher_id", "classroom_id", "created_at", "updated_at"}).
		AddRow(1, 1, 1, 1, 1, 1, 1, createdAt, updatedAt)

	mock.ExpectQuery(`SELECT`).
		WithArgs(1).
		WillReturnRows(rows)

	ctx := context.Background()
	schedules, err := repo.ListByClassID(ctx, 1)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if len(schedules) != 1 {
		t.Errorf("expected 1 schedule, got %d", len(schedules))
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}

func TestScheduleRepository_GetByClassAndWeekdayAndLesson(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("failed to create mock: %v", err)
	}
	defer db.Close()

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	repo := NewScheduleRepository(db, clock)

	createdAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	updatedAt := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)

	rows := sqlmock.NewRows([]string{"id", "class_id", "weekday_id", "lesson_number", "subject_id", "teacher_id", "classroom_id", "created_at", "updated_at"}).
		AddRow(1, 1, 1, 1, 1, 1, 1, createdAt, updatedAt)

	mock.ExpectQuery(`SELECT`).
		WithArgs(1, 1, 1).
		WillReturnRows(rows)

	ctx := context.Background()
	schedule, err := repo.GetByClassAndWeekdayAndLesson(ctx, 1, 1, 1)
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}

	if schedule == nil {
		t.Fatal("expected non-nil schedule")
	}

	if schedule.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", schedule.ID())
	}

	if err := mock.ExpectationsWereMet(); err != nil {
		t.Errorf("unmet expectations: %v", err)
	}
}
