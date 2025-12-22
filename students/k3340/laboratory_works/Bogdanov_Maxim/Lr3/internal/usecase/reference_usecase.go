package usecase

import (
	"context"
	"school-service/internal/domain"
	"school-service/internal/domain/repository"
	domainusecase "school-service/internal/domain/usecase"
)

var _ domainusecase.ReferenceUseCase = (*referenceUseCase)(nil)

// referenceUseCase реализация ReferenceUseCase
type referenceUseCase struct {
	referenceRepo repository.ReferenceRepository
}

// NewReferenceUseCase создает новый use case для справочных данных
func NewReferenceUseCase(referenceRepo repository.ReferenceRepository) domainusecase.ReferenceUseCase {
	return &referenceUseCase{
		referenceRepo: referenceRepo,
	}
}

// GetAllSubjects возвращает все предметы
func (uc *referenceUseCase) GetAllSubjects(ctx context.Context) ([]*domain.Subject, error) {
	return uc.referenceRepo.GetAllSubjects(ctx)
}

// GetAllClassrooms возвращает все кабинеты
func (uc *referenceUseCase) GetAllClassrooms(ctx context.Context) ([]*domain.Classroom, error) {
	return uc.referenceRepo.GetAllClassrooms(ctx)
}

// GetAllAcademicYears возвращает все учебные годы
func (uc *referenceUseCase) GetAllAcademicYears(ctx context.Context) ([]*domain.AcademicYear, error) {
	return uc.referenceRepo.GetAllAcademicYears(ctx)
}

// GetAllGradingPeriods возвращает все периоды оценивания
func (uc *referenceUseCase) GetAllGradingPeriods(ctx context.Context) ([]*domain.GradingPeriod, error) {
	return uc.referenceRepo.GetAllGradingPeriods(ctx)
}

// GetGradingPeriodsByAcademicYear возвращает периоды оценивания для учебного года
func (uc *referenceUseCase) GetGradingPeriodsByAcademicYear(ctx context.Context, academicYearID int) ([]*domain.GradingPeriod, error) {
	return uc.referenceRepo.GetGradingPeriodsByAcademicYear(ctx, academicYearID)
}

// GetAllWeekdays возвращает все дни недели
func (uc *referenceUseCase) GetAllWeekdays(ctx context.Context) ([]*domain.Weekday, error) {
	return uc.referenceRepo.GetAllWeekdays(ctx)
}
