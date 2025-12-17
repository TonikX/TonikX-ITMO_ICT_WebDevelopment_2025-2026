package repository

import (
	"context"

	"school-service/internal/domain"
)

// TeacherRepository интерфейс для работы с учителями
type TeacherRepository interface {
	// Create создает нового учителя
	Create(ctx context.Context, teacher *domain.Teacher) error

	// GetByID возвращает учителя по ID (включая удаленных)
	GetByID(ctx context.Context, id int) (*domain.Teacher, error)

	// GetByIDActive возвращает активного (не удаленного) учителя по ID
	GetByIDActive(ctx context.Context, id int) (*domain.Teacher, error)

	// Update обновляет данные учителя
	Update(ctx context.Context, teacher *domain.Teacher) error

	// Delete выполняет soft delete учителя
	Delete(ctx context.Context, id int) error

	// List возвращает список всех учителей (включая удаленных)
	List(ctx context.Context) ([]*domain.Teacher, error)

	// ListActive возвращает список активных (не удаленных) учителей
	ListActive(ctx context.Context) ([]*domain.Teacher, error)
}
