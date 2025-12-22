package usecase

import (
	"context"
	"errors"
	"testing"
	"time"

	"school-service/internal/domain"
	mockclock "school-service/internal/infrastructure/clock"
)

// mockClassRepository мок репозитория классов
type mockClassRepository struct {
	classes      map[int]*domain.Class
	createErr    error
	getByIDErr   error
	updateErr    error
	deleteErr    error
	listErr      error
	createCalled bool
	updateCalled bool
	deleteCalled bool
}

func newMockClassRepository() *mockClassRepository {
	return &mockClassRepository{
		classes: make(map[int]*domain.Class),
	}
}

func (m *mockClassRepository) Create(ctx context.Context, class *domain.Class) error {
	m.createCalled = true
	if m.createErr != nil {
		return m.createErr
	}
	class.SetID(len(m.classes) + 1)
	m.classes[class.ID()] = class
	return nil
}

func (m *mockClassRepository) GetByID(ctx context.Context, id int) (*domain.Class, error) {
	if m.getByIDErr != nil {
		return nil, m.getByIDErr
	}
	class, ok := m.classes[id]
	if !ok {
		return nil, domain.NewNotFoundError("Class", "id", id, "class not found")
	}
	return class, nil
}

func (m *mockClassRepository) GetByIDActive(ctx context.Context, id int) (*domain.Class, error) {
	return m.GetByID(ctx, id)
}

func (m *mockClassRepository) Update(ctx context.Context, class *domain.Class) error {
	m.updateCalled = true
	if m.updateErr != nil {
		return m.updateErr
	}
	if _, ok := m.classes[class.ID()]; !ok {
		return domain.NewNotFoundError("Class", "id", class.ID(), "class not found")
	}
	m.classes[class.ID()] = class
	return nil
}

func (m *mockClassRepository) Delete(ctx context.Context, id int) error {
	m.deleteCalled = true
	if m.deleteErr != nil {
		return m.deleteErr
	}
	if _, ok := m.classes[id]; !ok {
		return domain.NewNotFoundError("Class", "id", id, "class not found")
	}
	delete(m.classes, id)
	return nil
}

func (m *mockClassRepository) List(ctx context.Context) ([]*domain.Class, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	classes := make([]*domain.Class, 0, len(m.classes))
	for _, class := range m.classes {
		classes = append(classes, class)
	}
	return classes, nil
}

func (m *mockClassRepository) ListActive(ctx context.Context) ([]*domain.Class, error) {
	return m.List(ctx)
}

func (m *mockClassRepository) ListByAcademicYearID(ctx context.Context, academicYearID int) ([]*domain.Class, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	classes := make([]*domain.Class, 0)
	for _, class := range m.classes {
		if class.AcademicYearID() == academicYearID {
			classes = append(classes, class)
		}
	}
	return classes, nil
}

func TestClassUseCase_Create(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockClassRepository()
	mockLog := &mockLogger{}

	uc := NewClassUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	class, err := uc.Create(ctx, 10, "A", 1, nil)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if class == nil {
		t.Fatal("expected non-nil class")
	}

	if class.ID() == 0 {
		t.Error("expected class to have ID set")
	}

	if class.Grade() != 10 {
		t.Errorf("expected Grade = 10, got %d", class.Grade())
	}

	if class.Letter() != "A" {
		t.Errorf("expected Letter = A, got %s", class.Letter())
	}

	if !mockRepo.createCalled {
		t.Error("expected Create to be called on repository")
	}
}

func TestClassUseCase_GetByID(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockClassRepository()
	mockLog := &mockLogger{}

	existingClass, _ := domain.NewClass(mockClock, 10, "A", 1, nil)
	existingClass.SetID(1)
	mockRepo.classes[1] = existingClass

	uc := NewClassUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	class, err := uc.GetByID(ctx, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if class == nil {
		t.Fatal("expected non-nil class")
	}

	if class.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", class.ID())
	}
}

func TestClassUseCase_ListByAcademicYearID(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockClassRepository()
	mockLog := &mockLogger{}

	class1, _ := domain.NewClass(mockClock, 10, "A", 1, nil)
	class1.SetID(1)
	mockRepo.classes[1] = class1

	class2, _ := domain.NewClass(mockClock, 10, "B", 1, nil)
	class2.SetID(2)
	mockRepo.classes[2] = class2

	class3, _ := domain.NewClass(mockClock, 11, "A", 2, nil)
	class3.SetID(3)
	mockRepo.classes[3] = class3

	uc := NewClassUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	classes, err := uc.ListByAcademicYearID(ctx, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(classes) != 2 {
		t.Errorf("expected 2 classes, got %d", len(classes))
	}

	for _, class := range classes {
		if class.AcademicYearID() != 1 {
			t.Errorf("expected AcademicYearID = 1, got %d", class.AcademicYearID())
		}
	}
}

func TestClassUseCase_GetByID_NotFound(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockClassRepository()
	mockLog := &mockLogger{}

	uc := NewClassUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	class, err := uc.GetByID(ctx, 999)
	if err == nil {
		t.Error("expected error")
	}

	if class != nil {
		t.Errorf("expected nil class, got %v", class)
	}

	var domainErr *domain.Error
	if !errors.As(err, &domainErr) {
		t.Errorf("expected domain.Error, got %T", err)
	}
}
