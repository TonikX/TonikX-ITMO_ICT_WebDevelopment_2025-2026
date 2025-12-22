package usecase

import (
	"context"

	"school-service/internal/domain"
)

// TeacherUseCase интерфейс для бизнес-логики работы с учителями
type TeacherUseCase interface {
	// Create создает нового учителя
	Create(ctx context.Context, firstName, lastName string, middleName *string, classroomID *int) (*domain.Teacher, error)

	// GetByID возвращает учителя по ID
	GetByID(ctx context.Context, id int) (*domain.Teacher, error)

	// Update обновляет данные учителя
	Update(ctx context.Context, id int, firstName, lastName string, middleName *string, classroomID *int) (*domain.Teacher, error)

	// Delete удаляет учителя (soft delete)
	Delete(ctx context.Context, id int) error

	// List возвращает список всех активных учителей
	List(ctx context.Context) ([]*domain.Teacher, error)
}
