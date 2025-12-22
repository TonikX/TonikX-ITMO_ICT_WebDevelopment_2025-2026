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

var _ usecase.TeacherUseCase = (*TeacherUseCase)(nil)

// TeacherUseCase реализация бизнес-логики для учителей
type TeacherUseCase struct {
	repo   repository.TeacherRepository
	clock  clock.Clock
	logger logger.Logger
}

// NewTeacherUseCase создает новый usecase для учителей
func NewTeacherUseCase(repo repository.TeacherRepository, clock clock.Clock, logger logger.Logger) *TeacherUseCase {
	return &TeacherUseCase{
		repo:   repo,
		clock:  clock,
		logger: logger,
	}
}

// Create создает нового учителя
func (u *TeacherUseCase) Create(ctx context.Context, firstName, lastName string, middleName *string, classroomID *int) (*domain.Teacher, error) {
	teacher, err := domain.NewTeacher(u.clock, firstName, lastName, middleName, classroomID)
	if err != nil {
		return nil, fmt.Errorf("failed to create teacher: %w", err)
	}

	if err := u.repo.Create(ctx, teacher); err != nil {
		u.logger.Error("Failed to create teacher in repository", "error", err, "firstName", firstName, "lastName", lastName)
		return nil, fmt.Errorf("failed to save teacher: %w", err)
	}

	u.logger.Info("Teacher created", "id", teacher.ID(), "firstName", firstName, "lastName", lastName)
	return teacher, nil
}

// GetByID возвращает учителя по ID
func (u *TeacherUseCase) GetByID(ctx context.Context, id int) (*domain.Teacher, error) {
	teacher, err := u.repo.GetByIDActive(ctx, id)
	if err != nil {
		u.logger.Error("Failed to get teacher", "error", err, "id", id)
		return nil, err
	}

	return teacher, nil
}

// Update обновляет данные учителя
func (u *TeacherUseCase) Update(ctx context.Context, id int, firstName, lastName string, middleName *string, classroomID *int) (*domain.Teacher, error) {
	teacher, err := u.repo.GetByIDActive(ctx, id)
	if err != nil {
		return nil, err
	}

	teacher.SetFirstName(u.clock, firstName)
	teacher.SetLastName(u.clock, lastName)
	teacher.SetMiddleName(u.clock, middleName)
	teacher.SetClassroomID(u.clock, classroomID)

	if err := teacher.Validate(); err != nil {
		return nil, fmt.Errorf("validation failed: %w", err)
	}

	if err := u.repo.Update(ctx, teacher); err != nil {
		u.logger.Error("Failed to update teacher in repository", "error", err, "id", id)
		return nil, fmt.Errorf("failed to update teacher: %w", err)
	}

	u.logger.Info("Teacher updated", "id", id)
	return teacher, nil
}

// Delete удаляет учителя (soft delete)
func (u *TeacherUseCase) Delete(ctx context.Context, id int) error {
	if err := u.repo.Delete(ctx, id); err != nil {
		u.logger.Error("Failed to delete teacher", "error", err, "id", id)
		return err
	}

	u.logger.Info("Teacher deleted", "id", id)
	return nil
}

// List возвращает список всех активных учителей
func (u *TeacherUseCase) List(ctx context.Context) ([]*domain.Teacher, error) {
	teachers, err := u.repo.ListActive(ctx)
	if err != nil {
		u.logger.Error("Failed to list teachers", "error", err)
		return nil, fmt.Errorf("failed to list teachers: %w", err)
	}

	return teachers, nil
}
