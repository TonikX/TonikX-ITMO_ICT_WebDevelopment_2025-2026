package repository

import (
	"context"
)

// ReportRepository интерфейс для отчетов
type ReportRepository interface {
	// GetClassInfo возвращает информацию о классе
	GetClassInfo(ctx context.Context, classID int) (*ClassInfo, error)

	// GetStudentsCountByClass возвращает количество учеников в классе
	GetStudentsCountByClass(ctx context.Context, classID int) (int, error)

	// GetSubjectAverageGrades возвращает средние оценки по предметам для класса
	GetSubjectAverageGrades(ctx context.Context, classID int) ([]SubjectAverageGrade, error)

	// GetOverallAverageGrade возвращает общий средний балл по классу
	GetOverallAverageGrade(ctx context.Context, classID int) (float64, error)
}

// ClassInfo информация о классе
type ClassInfo struct {
	ID                int
	Name              string
	HomeroomTeacherID *int
}

// SubjectAverageGrade средняя оценка по предмету
type SubjectAverageGrade struct {
	SubjectID    int
	SubjectName  string
	AverageGrade float64
	GradesCount  int
}
