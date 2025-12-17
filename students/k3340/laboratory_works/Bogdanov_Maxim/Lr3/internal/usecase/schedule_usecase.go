package usecase

import (
	"context"
	"fmt"

	"school-service/internal/domain"
	"school-service/internal/domain/clock"
	"school-service/internal/domain/logger"
	"school-service/internal/domain/repository"
	"school-service/internal/domain/usecase"
)

var _ usecase.ScheduleUseCase = (*ScheduleUseCase)(nil)

// ScheduleUseCase реализация бизнес-логики для расписания
type ScheduleUseCase struct {
	repo   repository.ScheduleRepository
	clock  clock.Clock
	logger logger.Logger
}

// NewScheduleUseCase создает новый usecase для расписания
func NewScheduleUseCase(repo repository.ScheduleRepository, clock clock.Clock, logger logger.Logger) *ScheduleUseCase {
	return &ScheduleUseCase{
		repo:   repo,
		clock:  clock,
		logger: logger,
	}
}

// Create создает новую запись расписания
func (u *ScheduleUseCase) Create(ctx context.Context, classID, weekdayID, lessonNumber, subjectID, teacherID, classroomID int) (*domain.Schedule, error) {
	schedule, err := domain.NewSchedule(u.clock, classID, weekdayID, lessonNumber, subjectID, teacherID, classroomID)
	if err != nil {
		return nil, fmt.Errorf("failed to create schedule: %w", err)
	}

	if err := u.repo.Create(ctx, schedule); err != nil {
		u.logger.Error("Failed to create schedule in repository", "error", err, "classID", classID, "weekdayID", weekdayID, "lessonNumber", lessonNumber)
		return nil, fmt.Errorf("failed to save schedule: %w", err)
	}

	u.logger.Info("Schedule created", "id", schedule.ID(), "classID", classID, "weekdayID", weekdayID, "lessonNumber", lessonNumber)
	return schedule, nil
}

// GetByID возвращает запись расписания по ID
func (u *ScheduleUseCase) GetByID(ctx context.Context, id int) (*domain.Schedule, error) {
	schedule, err := u.repo.GetByID(ctx, id)
	if err != nil {
		u.logger.Error("Failed to get schedule", "error", err, "id", id)
		return nil, err
	}

	return schedule, nil
}

// Update обновляет запись расписания
func (u *ScheduleUseCase) Update(ctx context.Context, id int, classID, weekdayID, lessonNumber, subjectID, teacherID, classroomID int) (*domain.Schedule, error) {
	schedule, err := u.repo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}

	schedule.SetClassID(u.clock, classID)
	schedule.SetWeekdayID(u.clock, weekdayID)
	schedule.SetLessonNumber(u.clock, lessonNumber)
	schedule.SetSubjectID(u.clock, subjectID)
	schedule.SetTeacherID(u.clock, teacherID)
	schedule.SetClassroomID(u.clock, classroomID)

	if err := schedule.Validate(); err != nil {
		return nil, fmt.Errorf("validation failed: %w", err)
	}

	if err := u.repo.Update(ctx, schedule); err != nil {
		u.logger.Error("Failed to update schedule in repository", "error", err, "id", id)
		return nil, fmt.Errorf("failed to update schedule: %w", err)
	}

	u.logger.Info("Schedule updated", "id", id)
	return schedule, nil
}

// Delete удаляет запись расписания
func (u *ScheduleUseCase) Delete(ctx context.Context, id int) error {
	if err := u.repo.Delete(ctx, id); err != nil {
		u.logger.Error("Failed to delete schedule", "error", err, "id", id)
		return err
	}

	u.logger.Info("Schedule deleted", "id", id)
	return nil
}

// List возвращает список всех записей расписания
func (u *ScheduleUseCase) List(ctx context.Context) ([]*domain.Schedule, error) {
	schedules, err := u.repo.List(ctx)
	if err != nil {
		u.logger.Error("Failed to list schedules", "error", err)
		return nil, fmt.Errorf("failed to list schedules: %w", err)
	}

	return schedules, nil
}

// ListByClassID возвращает расписание для класса
func (u *ScheduleUseCase) ListByClassID(ctx context.Context, classID int) ([]*domain.Schedule, error) {
	schedules, err := u.repo.ListByClassID(ctx, classID)
	if err != nil {
		u.logger.Error("Failed to list schedules by class", "error", err, "classID", classID)
		return nil, fmt.Errorf("failed to list schedules by class: %w", err)
	}

	return schedules, nil
}

// GetByClassAndWeekdayAndLesson возвращает предмет в заданном классе, день недели и номер урока
func (u *ScheduleUseCase) GetByClassAndWeekdayAndLesson(ctx context.Context, classID, weekdayID, lessonNumber int) (*domain.Schedule, error) {
	schedule, err := u.repo.GetByClassAndWeekdayAndLesson(ctx, classID, weekdayID, lessonNumber)
	if err != nil {
		u.logger.Error("Failed to get schedule by class, weekday and lesson", "error", err, "classID", classID, "weekdayID", weekdayID, "lessonNumber", lessonNumber)
		return nil, err
	}

	return schedule, nil
}
