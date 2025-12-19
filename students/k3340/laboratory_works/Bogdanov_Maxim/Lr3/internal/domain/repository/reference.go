package repository

import (
	"context"
	"school-service/internal/domain"
)

// ReferenceRepository интерфейс для работы со справочными данными
type ReferenceRepository interface {
	// GetAllSubjects возвращает все предметы
	GetAllSubjects(ctx context.Context) ([]*domain.Subject, error)

	// GetAllClassrooms возвращает все кабинеты
	GetAllClassrooms(ctx context.Context) ([]*domain.Classroom, error)

	// GetAllAcademicYears возвращает все учебные годы
	GetAllAcademicYears(ctx context.Context) ([]*domain.AcademicYear, error)

	// GetAllGradingPeriods возвращает все периоды оценивания
	GetAllGradingPeriods(ctx context.Context) ([]*domain.GradingPeriod, error)

	// GetGradingPeriodsByAcademicYear возвращает периоды оценивания для учебного года
	GetGradingPeriodsByAcademicYear(ctx context.Context, academicYearID int) ([]*domain.GradingPeriod, error)

	// GetAllWeekdays возвращает все дни недели
	GetAllWeekdays(ctx context.Context) ([]*domain.Weekday, error)
}
