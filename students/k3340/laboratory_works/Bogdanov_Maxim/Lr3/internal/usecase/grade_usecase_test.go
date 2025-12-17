package usecase

import (
	"context"
	"errors"
	"testing"
	"time"

	"school-service/internal/domain"
	mockclock "school-service/internal/infrastructure/clock"
)

// mockGradeRepository мок репозитория оценок
type mockGradeRepository struct {
	grades       map[int]*domain.Grade
	createErr    error
	getByIDErr   error
	updateErr    error
	deleteErr    error
	listErr      error
	createCalled bool
	updateCalled bool
	deleteCalled bool
}

func newMockGradeRepository() *mockGradeRepository {
	return &mockGradeRepository{
		grades: make(map[int]*domain.Grade),
	}
}

func (m *mockGradeRepository) Create(ctx context.Context, grade *domain.Grade) error {
	m.createCalled = true
	if m.createErr != nil {
		return m.createErr
	}
	grade.SetID(len(m.grades) + 1)
	m.grades[grade.ID()] = grade
	return nil
}

func (m *mockGradeRepository) GetByID(ctx context.Context, id int) (*domain.Grade, error) {
	if m.getByIDErr != nil {
		return nil, m.getByIDErr
	}
	grade, ok := m.grades[id]
	if !ok {
		return nil, domain.NewNotFoundError("Grade", "id", id, "grade not found")
	}
	return grade, nil
}

func (m *mockGradeRepository) Update(ctx context.Context, grade *domain.Grade) error {
	m.updateCalled = true
	if m.updateErr != nil {
		return m.updateErr
	}
	if _, ok := m.grades[grade.ID()]; !ok {
		return domain.NewNotFoundError("Grade", "id", grade.ID(), "grade not found")
	}
	m.grades[grade.ID()] = grade
	return nil
}

func (m *mockGradeRepository) Delete(ctx context.Context, id int) error {
	m.deleteCalled = true
	if m.deleteErr != nil {
		return m.deleteErr
	}
	if _, ok := m.grades[id]; !ok {
		return domain.NewNotFoundError("Grade", "id", id, "grade not found")
	}
	delete(m.grades, id)
	return nil
}

func (m *mockGradeRepository) List(ctx context.Context) ([]*domain.Grade, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	grades := make([]*domain.Grade, 0, len(m.grades))
	for _, grade := range m.grades {
		grades = append(grades, grade)
	}
	return grades, nil
}

func (m *mockGradeRepository) ListByStudentID(ctx context.Context, studentID int) ([]*domain.Grade, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	grades := make([]*domain.Grade, 0)
	for _, grade := range m.grades {
		if grade.StudentID() == studentID {
			grades = append(grades, grade)
		}
	}
	return grades, nil
}

func (m *mockGradeRepository) ListByClassID(ctx context.Context, classID int) ([]*domain.Grade, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	return m.List(ctx)
}

func (m *mockGradeRepository) ListBySubjectID(ctx context.Context, subjectID int) ([]*domain.Grade, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	grades := make([]*domain.Grade, 0)
	for _, grade := range m.grades {
		if grade.SubjectID() == subjectID {
			grades = append(grades, grade)
		}
	}
	return grades, nil
}

func (m *mockGradeRepository) ListByClassAndSubject(ctx context.Context, classID, subjectID int) ([]*domain.Grade, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	return m.ListBySubjectID(ctx, subjectID)
}

func (m *mockGradeRepository) ListByClassAndGradingPeriod(ctx context.Context, classID, gradingPeriodID int) ([]*domain.Grade, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	grades := make([]*domain.Grade, 0)
	for _, grade := range m.grades {
		if grade.GradingPeriodID() == gradingPeriodID {
			grades = append(grades, grade)
		}
	}
	return grades, nil
}

func TestGradeUseCase_Create(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockGradeRepository()
	mockLog := &mockLogger{}

	uc := NewGradeUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	grade, err := uc.Create(ctx, 1, 1, 1, 5)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if grade == nil {
		t.Fatal("expected non-nil grade")
	}

	if grade.ID() == 0 {
		t.Error("expected non-zero ID")
	}

	if grade.Grade() != 5 {
		t.Errorf("expected Grade = 5, got %d", grade.Grade())
	}

	if !mockRepo.createCalled {
		t.Error("expected Create to be called on repository")
	}
}

func TestGradeUseCase_Create_InvalidGrade(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockGradeRepository()
	mockLog := &mockLogger{}

	uc := NewGradeUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	_, err := uc.Create(ctx, 1, 1, 1, 10) // Invalid grade (should be 1-5)
	if err == nil {
		t.Error("expected validation error")
	}
}

func TestGradeUseCase_GetByID(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockGradeRepository()
	mockLog := &mockLogger{}

	grade, _ := domain.NewGrade(mockClock, 1, 1, 1, 5)
	grade.SetID(1)
	mockRepo.grades[1] = grade

	uc := NewGradeUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	result, err := uc.GetByID(ctx, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if result == nil {
		t.Fatal("expected non-nil grade")
	}

	if result.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", result.ID())
	}
}

func TestGradeUseCase_GetByID_NotFound(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockGradeRepository()
	mockLog := &mockLogger{}

	uc := NewGradeUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	_, err := uc.GetByID(ctx, 999)
	if err == nil {
		t.Error("expected error")
	}

	var domainErr *domain.Error
	if !errors.As(err, &domainErr) {
		t.Errorf("expected domain.Error, got %T", err)
	}
}

func TestGradeUseCase_Update(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockGradeRepository()
	mockLog := &mockLogger{}

	grade, _ := domain.NewGrade(mockClock, 1, 1, 1, 4)
	grade.SetID(1)
	mockRepo.grades[1] = grade

	uc := NewGradeUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	updated, err := uc.Update(ctx, 1, 1, 1, 1, 5)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if updated.Grade() != 5 {
		t.Errorf("expected Grade = 5, got %d", updated.Grade())
	}

	if !mockRepo.updateCalled {
		t.Error("expected Update to be called on repository")
	}
}

func TestGradeUseCase_Delete(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockGradeRepository()
	mockLog := &mockLogger{}

	grade, _ := domain.NewGrade(mockClock, 1, 1, 1, 5)
	grade.SetID(1)
	mockRepo.grades[1] = grade

	uc := NewGradeUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	err := uc.Delete(ctx, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if !mockRepo.deleteCalled {
		t.Error("expected Delete to be called on repository")
	}
}

func TestGradeUseCase_List(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockGradeRepository()
	mockLog := &mockLogger{}

	grade1, _ := domain.NewGrade(mockClock, 1, 1, 1, 5)
	grade1.SetID(1)
	mockRepo.grades[1] = grade1

	grade2, _ := domain.NewGrade(mockClock, 2, 1, 1, 4)
	grade2.SetID(2)
	mockRepo.grades[2] = grade2

	uc := NewGradeUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	grades, err := uc.List(ctx)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(grades) != 2 {
		t.Errorf("expected 2 grades, got %d", len(grades))
	}
}

func TestGradeUseCase_ListByStudentID(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockGradeRepository()
	mockLog := &mockLogger{}

	grade1, _ := domain.NewGrade(mockClock, 1, 1, 1, 5)
	grade1.SetID(1)
	mockRepo.grades[1] = grade1

	grade2, _ := domain.NewGrade(mockClock, 2, 1, 1, 4)
	grade2.SetID(2)
	mockRepo.grades[2] = grade2

	uc := NewGradeUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	grades, err := uc.ListByStudentID(ctx, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(grades) != 1 {
		t.Errorf("expected 1 grade, got %d", len(grades))
	}
}
