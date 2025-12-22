package usecase

import (
	"context"
	"fmt"

	"school-service/internal/domain/logger"
	"school-service/internal/domain/repository"
	"school-service/internal/domain/usecase"
)

var _ usecase.ReportUseCase = (*ReportUseCase)(nil)

// ReportUseCase реализация бизнес-логики для отчетов
type ReportUseCase struct {
	reportRepo  repository.ReportRepository
	teacherRepo repository.TeacherRepository
	logger      logger.Logger
}

// NewReportUseCase создает новый usecase для отчетов
func NewReportUseCase(reportRepo repository.ReportRepository, teacherRepo repository.TeacherRepository, logger logger.Logger) *ReportUseCase {
	return &ReportUseCase{
		reportRepo:  reportRepo,
		teacherRepo: teacherRepo,
		logger:      logger,
	}
}

// GetClassPerformanceReport возвращает отчет об успеваемости класса
func (u *ReportUseCase) GetClassPerformanceReport(ctx context.Context, classID int) (*usecase.ClassPerformanceReport, error) {
	// Получаем информацию о классе
	classInfo, err := u.reportRepo.GetClassInfo(ctx, classID)
	if err != nil {
		u.logger.Error("Failed to get class info", "error", err, "classID", classID)
		return nil, fmt.Errorf("failed to get class info: %w", err)
	}

	// Получаем количество учеников
	studentsCount, err := u.reportRepo.GetStudentsCountByClass(ctx, classID)
	if err != nil {
		u.logger.Error("Failed to get students count", "error", err, "classID", classID)
		return nil, fmt.Errorf("failed to get students count: %w", err)
	}

	// Получаем информацию о классном руководителе
	var homeroomTeacher *usecase.HomeroomTeacherInfo
	if classInfo.HomeroomTeacherID != nil {
		teacher, err := u.teacherRepo.GetByIDActive(ctx, *classInfo.HomeroomTeacherID)
		if err != nil {
			u.logger.Warn("Failed to get homeroom teacher", "error", err, "teacherID", *classInfo.HomeroomTeacherID)
			// Не критично, продолжаем без классного руководителя
		} else {
			middleName := teacher.MiddleName()
			homeroomTeacher = &usecase.HomeroomTeacherInfo{
				ID:         teacher.ID(),
				FirstName:  teacher.FirstName(),
				LastName:   teacher.LastName(),
				MiddleName: middleName,
			}
		}
	}

	// Получаем средние оценки по предметам
	subjectPerformance, err := u.reportRepo.GetSubjectAverageGrades(ctx, classID)
	if err != nil {
		u.logger.Error("Failed to get subject average grades", "error", err, "classID", classID)
		return nil, fmt.Errorf("failed to get subject average grades: %w", err)
	}

	// Преобразуем в формат ответа
	subjectPerformanceInfo := make([]usecase.SubjectPerformanceInfo, 0, len(subjectPerformance))
	for _, sp := range subjectPerformance {
		subjectPerformanceInfo = append(subjectPerformanceInfo, usecase.SubjectPerformanceInfo{
			SubjectID:    sp.SubjectID,
			SubjectName:  sp.SubjectName,
			AverageGrade: sp.AverageGrade,
			GradesCount:  sp.GradesCount,
		})
	}

	// Получаем общий средний балл
	overallAverage, err := u.reportRepo.GetOverallAverageGrade(ctx, classID)
	if err != nil {
		u.logger.Error("Failed to get overall average grade", "error", err, "classID", classID)
		return nil, fmt.Errorf("failed to get overall average grade: %w", err)
	}

	report := &usecase.ClassPerformanceReport{
		ClassID:             classInfo.ID,
		ClassName:           classInfo.Name,
		StudentsCount:       studentsCount,
		HomeroomTeacher:     homeroomTeacher,
		OverallAverageGrade: overallAverage,
		SubjectPerformance:  subjectPerformanceInfo,
	}

	return report, nil
}
