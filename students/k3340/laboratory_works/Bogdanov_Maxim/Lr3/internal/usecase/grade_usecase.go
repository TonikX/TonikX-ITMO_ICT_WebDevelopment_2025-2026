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

var _ usecase.GradeUseCase = (*GradeUseCase)(nil)

// GradeUseCase реализация бизнес-логики для оценок
type GradeUseCase struct {
	repo   repository.GradeRepository
	clock  clock.Clock
	logger logger.Logger
}

// NewGradeUseCase создает новый usecase для оценок
func NewGradeUseCase(repo repository.GradeRepository, clock clock.Clock, logger logger.Logger) *GradeUseCase {
	return &GradeUseCase{
		repo:   repo,
		clock:  clock,
		logger: logger,
	}
}

// Create создает новую оценку
func (u *GradeUseCase) Create(ctx context.Context, studentID, subjectID, gradingPeriodID, grade int) (*domain.Grade, error) {
	gradeEntity, err := domain.NewGrade(u.clock, studentID, subjectID, gradingPeriodID, grade)
	if err != nil {
		return nil, fmt.Errorf("failed to create grade: %w", err)
	}

	if err := u.repo.Create(ctx, gradeEntity); err != nil {
		u.logger.Error("Failed to create grade in repository", "error", err, "studentID", studentID, "subjectID", subjectID, "grade", grade)
		return nil, fmt.Errorf("failed to save grade: %w", err)
	}

	u.logger.Info("Grade created", "id", gradeEntity.ID(), "studentID", studentID, "subjectID", subjectID, "grade", grade)
	return gradeEntity, nil
}

// GetByID возвращает оценку по ID
func (u *GradeUseCase) GetByID(ctx context.Context, id int) (*domain.Grade, error) {
	grade, err := u.repo.GetByID(ctx, id)
	if err != nil {
		u.logger.Error("Failed to get grade", "error", err, "id", id)
		return nil, err
	}

	return grade, nil
}

// Update обновляет оценку
func (u *GradeUseCase) Update(ctx context.Context, id int, studentID, subjectID, gradingPeriodID, grade int) (*domain.Grade, error) {
	gradeEntity, err := u.repo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}

	gradeEntity.SetStudentID(u.clock, studentID)
	gradeEntity.SetSubjectID(u.clock, subjectID)
	gradeEntity.SetGradingPeriodID(u.clock, gradingPeriodID)
	if err := gradeEntity.SetGrade(u.clock, grade); err != nil {
		return nil, fmt.Errorf("validation failed: %w", err)
	}

	if err := gradeEntity.Validate(); err != nil {
		return nil, fmt.Errorf("validation failed: %w", err)
	}

	if err := u.repo.Update(ctx, gradeEntity); err != nil {
		u.logger.Error("Failed to update grade in repository", "error", err, "id", id)
		return nil, fmt.Errorf("failed to update grade: %w", err)
	}

	u.logger.Info("Grade updated", "id", id)
	return gradeEntity, nil
}

// Delete удаляет оценку
func (u *GradeUseCase) Delete(ctx context.Context, id int) error {
	if err := u.repo.Delete(ctx, id); err != nil {
		u.logger.Error("Failed to delete grade", "error", err, "id", id)
		return err
	}

	u.logger.Info("Grade deleted", "id", id)
	return nil
}

// List возвращает список всех оценок
func (u *GradeUseCase) List(ctx context.Context) ([]*domain.Grade, error) {
	grades, err := u.repo.List(ctx)
	if err != nil {
		u.logger.Error("Failed to list grades", "error", err)
		return nil, fmt.Errorf("failed to list grades: %w", err)
	}

	return grades, nil
}

// ListByStudentID возвращает оценки ученика
func (u *GradeUseCase) ListByStudentID(ctx context.Context, studentID int) ([]*domain.Grade, error) {
	grades, err := u.repo.ListByStudentID(ctx, studentID)
	if err != nil {
		u.logger.Error("Failed to list grades by student", "error", err, "studentID", studentID)
		return nil, fmt.Errorf("failed to list grades by student: %w", err)
	}

	return grades, nil
}

// ListByClassID возвращает оценки всех учеников класса
func (u *GradeUseCase) ListByClassID(ctx context.Context, classID int) ([]*domain.Grade, error) {
	grades, err := u.repo.ListByClassID(ctx, classID)
	if err != nil {
		u.logger.Error("Failed to list grades by class", "error", err, "classID", classID)
		return nil, fmt.Errorf("failed to list grades by class: %w", err)
	}

	return grades, nil
}

// ListBySubjectID возвращает оценки по предмету
func (u *GradeUseCase) ListBySubjectID(ctx context.Context, subjectID int) ([]*domain.Grade, error) {
	grades, err := u.repo.ListBySubjectID(ctx, subjectID)
	if err != nil {
		u.logger.Error("Failed to list grades by subject", "error", err, "subjectID", subjectID)
		return nil, fmt.Errorf("failed to list grades by subject: %w", err)
	}

	return grades, nil
}

// ListByClassAndSubject возвращает оценки класса по предмету
func (u *GradeUseCase) ListByClassAndSubject(ctx context.Context, classID, subjectID int) ([]*domain.Grade, error) {
	grades, err := u.repo.ListByClassAndSubject(ctx, classID, subjectID)
	if err != nil {
		u.logger.Error("Failed to list grades by class and subject", "error", err, "classID", classID, "subjectID", subjectID)
		return nil, fmt.Errorf("failed to list grades by class and subject: %w", err)
	}

	return grades, nil
}

// ListByClassAndGradingPeriod возвращает оценки класса за оценочный период
func (u *GradeUseCase) ListByClassAndGradingPeriod(ctx context.Context, classID, gradingPeriodID int) ([]*domain.Grade, error) {
	grades, err := u.repo.ListByClassAndGradingPeriod(ctx, classID, gradingPeriodID)
	if err != nil {
		u.logger.Error("Failed to list grades by class and grading period", "error", err, "classID", classID, "gradingPeriodID", gradingPeriodID)
		return nil, fmt.Errorf("failed to list grades by class and grading period: %w", err)
	}

	return grades, nil
}
