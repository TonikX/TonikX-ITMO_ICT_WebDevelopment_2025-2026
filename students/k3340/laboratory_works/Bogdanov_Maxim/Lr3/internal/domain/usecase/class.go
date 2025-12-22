package usecase

import (
	"context"

	"school-service/internal/domain"
)

// ClassUseCase интерфейс для бизнес-логики работы с классами
type ClassUseCase interface {
	// Create создает новый класс
	Create(ctx context.Context, grade int, letter string, academicYearID int, classTeacherID *int) (*domain.Class, error)

	// GetByID возвращает класс по ID
	GetByID(ctx context.Context, id int) (*domain.Class, error)

	// Update обновляет данные класса
	Update(ctx context.Context, id int, grade int, letter string, academicYearID int, classTeacherID *int) (*domain.Class, error)

	// Delete удаляет класс (soft delete)
	Delete(ctx context.Context, id int) error

	// List возвращает список всех активных классов
	List(ctx context.Context) ([]*domain.Class, error)

	// ListByAcademicYearID возвращает список классов учебного года
	ListByAcademicYearID(ctx context.Context, academicYearID int) ([]*domain.Class, error)
}
