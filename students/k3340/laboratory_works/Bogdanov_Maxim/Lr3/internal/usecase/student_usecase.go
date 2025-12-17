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

var _ usecase.StudentUseCase = (*StudentUseCase)(nil)

// StudentUseCase реализация бизнес-логики для учеников
type StudentUseCase struct {
	repo   repository.StudentRepository
	clock  clock.Clock
	logger logger.Logger
}

// NewStudentUseCase создает новый usecase для учеников
func NewStudentUseCase(repo repository.StudentRepository, clock clock.Clock, logger logger.Logger) *StudentUseCase {
	return &StudentUseCase{
		repo:   repo,
		clock:  clock,
		logger: logger,
	}
}

// Create создает нового ученика
func (u *StudentUseCase) Create(ctx context.Context, firstName, lastName string, middleName *string, genderID, classID int) (*domain.Student, error) {
	student, err := domain.NewStudent(u.clock, firstName, lastName, middleName, genderID, classID)
	if err != nil {
		return nil, fmt.Errorf("failed to create student: %w", err)
	}

	if err := u.repo.Create(ctx, student); err != nil {
		u.logger.Error("Failed to create student in repository", "error", err, "firstName", firstName, "lastName", lastName)
		return nil, fmt.Errorf("failed to save student: %w", err)
	}

	u.logger.Info("Student created", "id", student.ID(), "firstName", firstName, "lastName", lastName)
	return student, nil
}

// GetByID возвращает ученика по ID
func (u *StudentUseCase) GetByID(ctx context.Context, id int) (*domain.Student, error) {
	student, err := u.repo.GetByIDActive(ctx, id)
	if err != nil {
		u.logger.Error("Failed to get student", "error", err, "id", id)
		return nil, err
	}

	return student, nil
}

// Update обновляет данные ученика
func (u *StudentUseCase) Update(ctx context.Context, id int, firstName, lastName string, middleName *string, genderID, classID int) (*domain.Student, error) {
	student, err := u.repo.GetByIDActive(ctx, id)
	if err != nil {
		return nil, err
	}

	student.SetFirstName(u.clock, firstName)
	student.SetLastName(u.clock, lastName)
	student.SetMiddleName(u.clock, middleName)
	student.SetGenderID(u.clock, genderID)
	student.SetClassID(u.clock, classID)

	if err := student.Validate(); err != nil {
		return nil, fmt.Errorf("validation failed: %w", err)
	}

	if err := u.repo.Update(ctx, student); err != nil {
		u.logger.Error("Failed to update student in repository", "error", err, "id", id)
		return nil, fmt.Errorf("failed to update student: %w", err)
	}

	u.logger.Info("Student updated", "id", id)
	return student, nil
}

// Delete удаляет ученика (soft delete)
func (u *StudentUseCase) Delete(ctx context.Context, id int) error {
	if err := u.repo.Delete(ctx, id); err != nil {
		u.logger.Error("Failed to delete student", "error", err, "id", id)
		return err
	}

	u.logger.Info("Student deleted", "id", id)
	return nil
}

// List возвращает список всех активных учеников
func (u *StudentUseCase) List(ctx context.Context) ([]*domain.Student, error) {
	students, err := u.repo.ListActive(ctx)
	if err != nil {
		u.logger.Error("Failed to list students", "error", err)
		return nil, fmt.Errorf("failed to list students: %w", err)
	}

	return students, nil
}

// ListByClassID возвращает список активных учеников класса
func (u *StudentUseCase) ListByClassID(ctx context.Context, classID int) ([]*domain.Student, error) {
	students, err := u.repo.ListActiveByClassID(ctx, classID)
	if err != nil {
		u.logger.Error("Failed to list students by class", "error", err, "classID", classID)
		return nil, fmt.Errorf("failed to list students by class: %w", err)
	}

	return students, nil
}
