package usecase

import (
	"context"

	"school-service/internal/domain"
)

// StudentUseCase интерфейс для бизнес-логики работы с учениками
type StudentUseCase interface {
	// Create создает нового ученика
	Create(ctx context.Context, firstName, lastName string, middleName *string, genderID, classID int) (*domain.Student, error)

	// GetByID возвращает ученика по ID
	GetByID(ctx context.Context, id int) (*domain.Student, error)

	// Update обновляет данные ученика
	Update(ctx context.Context, id int, firstName, lastName string, middleName *string, genderID, classID int) (*domain.Student, error)

	// Delete удаляет ученика (soft delete)
	Delete(ctx context.Context, id int) error

	// List возвращает список всех активных учеников
	List(ctx context.Context) ([]*domain.Student, error)

	// ListByClassID возвращает список активных учеников класса
	ListByClassID(ctx context.Context, classID int) ([]*domain.Student, error)
}
