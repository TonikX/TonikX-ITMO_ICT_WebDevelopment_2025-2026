package repository

import (
	"context"

	"school-service/internal/domain"
)

// StudentRepository интерфейс для работы с учениками
type StudentRepository interface {
	// Create создает нового ученика
	Create(ctx context.Context, student *domain.Student) error

	// GetByID возвращает ученика по ID (включая удаленных)
	GetByID(ctx context.Context, id int) (*domain.Student, error)

	// GetByIDActive возвращает активного (не удаленного) ученика по ID
	GetByIDActive(ctx context.Context, id int) (*domain.Student, error)

	// Update обновляет данные ученика
	Update(ctx context.Context, student *domain.Student) error

	// Delete выполняет soft delete ученика
	Delete(ctx context.Context, id int) error

	// List возвращает список всех учеников (включая удаленных)
	List(ctx context.Context) ([]*domain.Student, error)

	// ListActive возвращает список активных (не удаленных) учеников
	ListActive(ctx context.Context) ([]*domain.Student, error)

	// ListByClassID возвращает список учеников класса
	ListByClassID(ctx context.Context, classID int) ([]*domain.Student, error)

	// ListActiveByClassID возвращает список активных учеников класса
	ListActiveByClassID(ctx context.Context, classID int) ([]*domain.Student, error)
}
