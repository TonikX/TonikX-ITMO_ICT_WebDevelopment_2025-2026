package usecase

import (
	"context"
	"school-service/internal/domain"
)

// ReferenceUseCase интерфейс для работы со справочными данными
type ReferenceUseCase interface {
	GetAllSubjects(ctx context.Context) ([]*domain.Subject, error)
	GetAllClassrooms(ctx context.Context) ([]*domain.Classroom, error)
	GetAllAcademicYears(ctx context.Context) ([]*domain.AcademicYear, error)
	GetAllGradingPeriods(ctx context.Context) ([]*domain.GradingPeriod, error)
	GetGradingPeriodsByAcademicYear(ctx context.Context, academicYearID int) ([]*domain.GradingPeriod, error)
	GetAllWeekdays(ctx context.Context) ([]*domain.Weekday, error)
}
