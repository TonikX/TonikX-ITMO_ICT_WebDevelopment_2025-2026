package usecase

import (
	"context"
)

// ReportUseCase интерфейс для отчетов
type ReportUseCase interface {
	// GetClassPerformanceReport возвращает отчет об успеваемости класса
	GetClassPerformanceReport(ctx context.Context, classID int) (*ClassPerformanceReport, error)
}

// ClassPerformanceReport отчет об успеваемости класса
type ClassPerformanceReport struct {
	ClassID             int                      `json:"class_id"`
	ClassName           string                   `json:"class_name"`
	StudentsCount       int                      `json:"students_count"`
	HomeroomTeacher     *HomeroomTeacherInfo     `json:"homeroom_teacher"`
	OverallAverageGrade float64                  `json:"overall_average_grade"`
	SubjectPerformance  []SubjectPerformanceInfo `json:"subject_performance"`
}

// HomeroomTeacherInfo информация о классном руководителе
type HomeroomTeacherInfo struct {
	ID         int     `json:"id"`
	FirstName  string  `json:"first_name"`
	LastName   string  `json:"last_name"`
	MiddleName *string `json:"middle_name,omitempty"`
}

// SubjectPerformanceInfo информация об успеваемости по предмету
type SubjectPerformanceInfo struct {
	SubjectID    int     `json:"subject_id"`
	SubjectName  string  `json:"subject_name"`
	AverageGrade float64 `json:"average_grade"`
	GradesCount  int     `json:"grades_count"`
}
