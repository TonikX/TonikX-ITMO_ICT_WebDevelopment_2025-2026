package usecase

import (
	"context"
	"errors"
	"testing"
	"time"

	"school-service/internal/domain"
	"school-service/internal/domain/repository"
	mockclock "school-service/internal/infrastructure/clock"
)

// mockReportRepository мок репозитория для отчетов
type mockReportRepository struct {
	classInfo            map[int]*repository.ClassInfo
	studentsCount        map[int]int
	subjectAverageGrades map[int][]repository.SubjectAverageGrade
	overallAverage       map[int]float64
	err                  error
}

func newMockReportRepository() *mockReportRepository {
	return &mockReportRepository{
		classInfo:            make(map[int]*repository.ClassInfo),
		studentsCount:        make(map[int]int),
		subjectAverageGrades: make(map[int][]repository.SubjectAverageGrade),
		overallAverage:       make(map[int]float64),
	}
}

func (m *mockReportRepository) GetClassInfo(ctx context.Context, classID int) (*repository.ClassInfo, error) {
	if m.err != nil {
		return nil, m.err
	}
	info, ok := m.classInfo[classID]
	if !ok {
		return nil, errors.New("class not found")
	}
	return info, nil
}

func (m *mockReportRepository) GetStudentsCountByClass(ctx context.Context, classID int) (int, error) {
	if m.err != nil {
		return 0, m.err
	}
	return m.studentsCount[classID], nil
}

func (m *mockReportRepository) GetSubjectAverageGrades(ctx context.Context, classID int) ([]repository.SubjectAverageGrade, error) {
	if m.err != nil {
		return nil, m.err
	}
	return m.subjectAverageGrades[classID], nil
}

func (m *mockReportRepository) GetOverallAverageGrade(ctx context.Context, classID int) (float64, error) {
	if m.err != nil {
		return 0, m.err
	}
	return m.overallAverage[classID], nil
}

func TestReportUseCase_GetClassPerformanceReport(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockReportRepo := newMockReportRepository()
	mockTeacherRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	// Настраиваем данные класса
	teacherID := 1
	mockReportRepo.classInfo[1] = &repository.ClassInfo{
		ID:                1,
		Name:              "5A",
		HomeroomTeacherID: &teacherID,
	}
	mockReportRepo.studentsCount[1] = 25
	mockReportRepo.overallAverage[1] = 4.2
	mockReportRepo.subjectAverageGrades[1] = []repository.SubjectAverageGrade{
		{SubjectID: 1, SubjectName: "Math", AverageGrade: 4.5, GradesCount: 50},
		{SubjectID: 2, SubjectName: "Physics", AverageGrade: 4.0, GradesCount: 40},
	}

	// Создаем классного руководителя
	teacher, _ := domain.NewTeacher(mockClock, "John", "Doe", nil, nil)
	teacher.SetID(1)
	mockTeacherRepo.teachers[1] = teacher

	uc := NewReportUseCase(mockReportRepo, mockTeacherRepo, mockLog)

	ctx := context.Background()
	report, err := uc.GetClassPerformanceReport(ctx, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if report == nil {
		t.Fatal("expected non-nil report")
	}

	if report.ClassID != 1 {
		t.Errorf("expected ClassID = 1, got %d", report.ClassID)
	}

	if report.StudentsCount != 25 {
		t.Errorf("expected StudentsCount = 25, got %d", report.StudentsCount)
	}

	if report.OverallAverageGrade != 4.2 {
		t.Errorf("expected OverallAverageGrade = 4.2, got %f", report.OverallAverageGrade)
	}

	if len(report.SubjectPerformance) != 2 {
		t.Errorf("expected 2 subjects, got %d", len(report.SubjectPerformance))
	}

	if report.HomeroomTeacher == nil {
		t.Error("expected non-nil homeroom teacher")
	}

	if report.HomeroomTeacher.ID != 1 {
		t.Errorf("expected HomeroomTeacher.ID = 1, got %d", report.HomeroomTeacher.ID)
	}
}

func TestReportUseCase_GetClassPerformanceReport_NoHomeroomTeacher(t *testing.T) {
	mockReportRepo := newMockReportRepository()
	mockTeacherRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	// Класс без классного руководителя
	mockReportRepo.classInfo[1] = &repository.ClassInfo{
		ID:                1,
		Name:              "5A",
		HomeroomTeacherID: nil,
	}
	mockReportRepo.studentsCount[1] = 25
	mockReportRepo.overallAverage[1] = 4.2
	mockReportRepo.subjectAverageGrades[1] = []repository.SubjectAverageGrade{}

	uc := NewReportUseCase(mockReportRepo, mockTeacherRepo, mockLog)

	ctx := context.Background()
	report, err := uc.GetClassPerformanceReport(ctx, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if report.HomeroomTeacher != nil {
		t.Error("expected nil homeroom teacher")
	}
}

func TestReportUseCase_GetClassPerformanceReport_ClassNotFound(t *testing.T) {
	mockReportRepo := newMockReportRepository()
	mockTeacherRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	mockReportRepo.err = errors.New("class not found")

	uc := NewReportUseCase(mockReportRepo, mockTeacherRepo, mockLog)

	ctx := context.Background()
	_, err := uc.GetClassPerformanceReport(ctx, 999)
	if err == nil {
		t.Error("expected error")
	}
}

func TestReportUseCase_GetClassPerformanceReport_HomeroomTeacherNotFound(t *testing.T) {
	mockReportRepo := newMockReportRepository()
	mockTeacherRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	// Класс с несуществующим классным руководителем
	teacherID := 999
	mockReportRepo.classInfo[1] = &repository.ClassInfo{
		ID:                1,
		Name:              "5A",
		HomeroomTeacherID: &teacherID,
	}
	mockReportRepo.studentsCount[1] = 25
	mockReportRepo.overallAverage[1] = 4.2
	mockReportRepo.subjectAverageGrades[1] = []repository.SubjectAverageGrade{}

	uc := NewReportUseCase(mockReportRepo, mockTeacherRepo, mockLog)

	ctx := context.Background()
	report, err := uc.GetClassPerformanceReport(ctx, 1)
	// Не должно быть ошибки, просто классный руководитель будет nil
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if report.HomeroomTeacher != nil {
		t.Error("expected nil homeroom teacher when teacher not found")
	}
}
