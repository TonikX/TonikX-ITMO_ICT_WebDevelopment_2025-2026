package repository

import (
	"context"

	"school-service/internal/domain"
)

// ScheduleRepository интерфейс для работы с расписанием
type ScheduleRepository interface {
	// Create создает новую запись расписания
	Create(ctx context.Context, schedule *domain.Schedule) error

	// GetByID возвращает запись расписания по ID
	GetByID(ctx context.Context, id int) (*domain.Schedule, error)

	// Update обновляет запись расписания
	Update(ctx context.Context, schedule *domain.Schedule) error

	// Delete удаляет запись расписания
	Delete(ctx context.Context, id int) error

	// List возвращает список всех записей расписания
	List(ctx context.Context) ([]*domain.Schedule, error)

	// ListByClassID возвращает расписание для класса
	ListByClassID(ctx context.Context, classID int) ([]*domain.Schedule, error)

	// GetByClassAndWeekdayAndLesson возвращает предмет в заданном классе, день недели и номер урока
	GetByClassAndWeekdayAndLesson(ctx context.Context, classID, weekdayID, lessonNumber int) (*domain.Schedule, error)
}
