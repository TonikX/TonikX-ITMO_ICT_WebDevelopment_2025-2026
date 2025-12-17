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

var _ usecase.ClassUseCase = (*ClassUseCase)(nil)

// ClassUseCase реализация бизнес-логики для классов
type ClassUseCase struct {
	repo   repository.ClassRepository
	clock  clock.Clock
	logger logger.Logger
}

// NewClassUseCase создает новый usecase для классов
func NewClassUseCase(repo repository.ClassRepository, clock clock.Clock, logger logger.Logger) *ClassUseCase {
	return &ClassUseCase{
		repo:   repo,
		clock:  clock,
		logger: logger,
	}
}

// Create создает новый класс
func (u *ClassUseCase) Create(ctx context.Context, grade int, letter string, academicYearID int, classTeacherID *int) (*domain.Class, error) {
	class, err := domain.NewClass(u.clock, grade, letter, academicYearID, classTeacherID)
	if err != nil {
		return nil, fmt.Errorf("failed to create class: %w", err)
	}

	if err := u.repo.Create(ctx, class); err != nil {
		u.logger.Error("Failed to create class in repository", "error", err, "grade", grade, "letter", letter)
		return nil, fmt.Errorf("failed to save class: %w", err)
	}

	u.logger.Info("Class created", "id", class.ID(), "grade", grade, "letter", letter)
	return class, nil
}

// GetByID возвращает класс по ID
func (u *ClassUseCase) GetByID(ctx context.Context, id int) (*domain.Class, error) {
	class, err := u.repo.GetByIDActive(ctx, id)
	if err != nil {
		u.logger.Error("Failed to get class", "error", err, "id", id)
		return nil, err
	}

	return class, nil
}

// Update обновляет данные класса
func (u *ClassUseCase) Update(ctx context.Context, id int, grade int, letter string, academicYearID int, classTeacherID *int) (*domain.Class, error) {
	class, err := u.repo.GetByIDActive(ctx, id)
	if err != nil {
		return nil, err
	}

	class.SetGrade(u.clock, grade)
	class.SetLetter(u.clock, letter)
	class.SetAcademicYearID(u.clock, academicYearID)
	class.SetClassTeacherID(u.clock, classTeacherID)

	if err := class.Validate(); err != nil {
		return nil, fmt.Errorf("validation failed: %w", err)
	}

	if err := u.repo.Update(ctx, class); err != nil {
		u.logger.Error("Failed to update class in repository", "error", err, "id", id)
		return nil, fmt.Errorf("failed to update class: %w", err)
	}

	u.logger.Info("Class updated", "id", id)
	return class, nil
}

// Delete удаляет класс (soft delete)
func (u *ClassUseCase) Delete(ctx context.Context, id int) error {
	if err := u.repo.Delete(ctx, id); err != nil {
		u.logger.Error("Failed to delete class", "error", err, "id", id)
		return err
	}

	u.logger.Info("Class deleted", "id", id)
	return nil
}

// List возвращает список всех активных классов
func (u *ClassUseCase) List(ctx context.Context) ([]*domain.Class, error) {
	classes, err := u.repo.ListActive(ctx)
	if err != nil {
		u.logger.Error("Failed to list classes", "error", err)
		return nil, fmt.Errorf("failed to list classes: %w", err)
	}

	return classes, nil
}

// ListByAcademicYearID возвращает список классов учебного года
func (u *ClassUseCase) ListByAcademicYearID(ctx context.Context, academicYearID int) ([]*domain.Class, error) {
	classes, err := u.repo.ListByAcademicYearID(ctx, academicYearID)
	if err != nil {
		u.logger.Error("Failed to list classes by academic year", "error", err, "academicYearID", academicYearID)
		return nil, fmt.Errorf("failed to list classes by academic year: %w", err)
	}

	return classes, nil
}
