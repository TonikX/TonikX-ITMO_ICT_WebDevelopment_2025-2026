package usecase

import (
	"context"

	"school-service/internal/domain"
)

// GradeUseCase интерфейс для бизнес-логики работы с оценками
type GradeUseCase interface {
	// Create создает новую оценку
	Create(ctx context.Context, studentID, subjectID, gradingPeriodID, grade int) (*domain.Grade, error)

	// GetByID возвращает оценку по ID
	GetByID(ctx context.Context, id int) (*domain.Grade, error)

	// Update обновляет оценку
	Update(ctx context.Context, id int, studentID, subjectID, gradingPeriodID, grade int) (*domain.Grade, error)

	// Delete удаляет оценку
	Delete(ctx context.Context, id int) error

	// List возвращает список всех оценок
	List(ctx context.Context) ([]*domain.Grade, error)

	// ListByStudentID возвращает оценки ученика
	ListByStudentID(ctx context.Context, studentID int) ([]*domain.Grade, error)

	// ListByClassID возвращает оценки всех учеников класса
	ListByClassID(ctx context.Context, classID int) ([]*domain.Grade, error)

	// ListBySubjectID возвращает оценки по предмету
	ListBySubjectID(ctx context.Context, subjectID int) ([]*domain.Grade, error)

	// ListByClassAndSubject возвращает оценки класса по предмету
	ListByClassAndSubject(ctx context.Context, classID, subjectID int) ([]*domain.Grade, error)

	// ListByClassAndGradingPeriod возвращает оценки класса за оценочный период
	ListByClassAndGradingPeriod(ctx context.Context, classID, gradingPeriodID int) ([]*domain.Grade, error)
}
