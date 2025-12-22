package repository

import (
	"context"

	"school-service/internal/domain"
)

// ClassRepository интерфейс для работы с классами
type ClassRepository interface {
	// Create создает новый класс
	Create(ctx context.Context, class *domain.Class) error

	// GetByID возвращает класс по ID (включая удаленные)
	GetByID(ctx context.Context, id int) (*domain.Class, error)

	// GetByIDActive возвращает активный (не удаленный) класс по ID
	GetByIDActive(ctx context.Context, id int) (*domain.Class, error)

	// Update обновляет данные класса
	Update(ctx context.Context, class *domain.Class) error

	// Delete выполняет soft delete класса
	Delete(ctx context.Context, id int) error

	// List возвращает список всех классов (включая удаленные)
	List(ctx context.Context) ([]*domain.Class, error)

	// ListActive возвращает список активных (не удаленных) классов
	ListActive(ctx context.Context) ([]*domain.Class, error)

	// ListByAcademicYearID возвращает список классов учебного года
	ListByAcademicYearID(ctx context.Context, academicYearID int) ([]*domain.Class, error)
}
