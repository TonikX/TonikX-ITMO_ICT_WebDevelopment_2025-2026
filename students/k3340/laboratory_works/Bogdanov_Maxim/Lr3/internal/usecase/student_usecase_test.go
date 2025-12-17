package usecase

import (
	"context"
	"testing"
	"time"

	"school-service/internal/domain"
	mockclock "school-service/internal/infrastructure/clock"
)

// mockStudentRepository мок репозитория учеников
type mockStudentRepository struct {
	students     map[int]*domain.Student
	createErr    error
	getByIDErr   error
	updateErr    error
	deleteErr    error
	listErr      error
	createCalled bool
	updateCalled bool
	deleteCalled bool
}

func newMockStudentRepository() *mockStudentRepository {
	return &mockStudentRepository{
		students: make(map[int]*domain.Student),
	}
}

func (m *mockStudentRepository) Create(ctx context.Context, student *domain.Student) error {
	m.createCalled = true
	if m.createErr != nil {
		return m.createErr
	}
	student.SetID(len(m.students) + 1)
	m.students[student.ID()] = student
	return nil
}

func (m *mockStudentRepository) GetByID(ctx context.Context, id int) (*domain.Student, error) {
	if m.getByIDErr != nil {
		return nil, m.getByIDErr
	}
	student, ok := m.students[id]
	if !ok {
		return nil, domain.NewNotFoundError("Student", "id", id, "student not found")
	}
	return student, nil
}

func (m *mockStudentRepository) GetByIDActive(ctx context.Context, id int) (*domain.Student, error) {
	return m.GetByID(ctx, id)
}

func (m *mockStudentRepository) Update(ctx context.Context, student *domain.Student) error {
	m.updateCalled = true
	if m.updateErr != nil {
		return m.updateErr
	}
	if _, ok := m.students[student.ID()]; !ok {
		return domain.NewNotFoundError("Student", "id", student.ID(), "student not found")
	}
	m.students[student.ID()] = student
	return nil
}

func (m *mockStudentRepository) Delete(ctx context.Context, id int) error {
	m.deleteCalled = true
	if m.deleteErr != nil {
		return m.deleteErr
	}
	if _, ok := m.students[id]; !ok {
		return domain.NewNotFoundError("Student", "id", id, "student not found")
	}
	delete(m.students, id)
	return nil
}

func (m *mockStudentRepository) List(ctx context.Context) ([]*domain.Student, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	students := make([]*domain.Student, 0, len(m.students))
	for _, student := range m.students {
		students = append(students, student)
	}
	return students, nil
}

func (m *mockStudentRepository) ListActive(ctx context.Context) ([]*domain.Student, error) {
	return m.List(ctx)
}

func (m *mockStudentRepository) ListByClassID(ctx context.Context, classID int) ([]*domain.Student, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	students := make([]*domain.Student, 0)
	for _, student := range m.students {
		if student.ClassID() == classID {
			students = append(students, student)
		}
	}
	return students, nil
}

func (m *mockStudentRepository) ListActiveByClassID(ctx context.Context, classID int) ([]*domain.Student, error) {
	return m.ListByClassID(ctx, classID)
}

func TestStudentUseCase_Create(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockStudentRepository()
	mockLog := &mockLogger{}

	uc := NewStudentUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	student, err := uc.Create(ctx, "John", "Doe", nil, 1, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if student == nil {
		t.Fatal("expected non-nil student")
	}

	if student.ID() == 0 {
		t.Error("expected student to have ID set")
	}

	if student.FirstName() != "John" {
		t.Errorf("expected FirstName = John, got %s", student.FirstName())
	}

	if !mockRepo.createCalled {
		t.Error("expected Create to be called on repository")
	}
}

func TestStudentUseCase_GetByID(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockStudentRepository()
	mockLog := &mockLogger{}

	existingStudent, _ := domain.NewStudent(mockClock, "John", "Doe", nil, 1, 1)
	existingStudent.SetID(1)
	mockRepo.students[1] = existingStudent

	uc := NewStudentUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	student, err := uc.GetByID(ctx, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if student == nil {
		t.Fatal("expected non-nil student")
	}

	if student.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", student.ID())
	}
}

func TestStudentUseCase_ListByClassID(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockStudentRepository()
	mockLog := &mockLogger{}

	student1, _ := domain.NewStudent(mockClock, "John", "Doe", nil, 1, 5)
	student1.SetID(1)
	mockRepo.students[1] = student1

	student2, _ := domain.NewStudent(mockClock, "Jane", "Smith", nil, 2, 5)
	student2.SetID(2)
	mockRepo.students[2] = student2

	student3, _ := domain.NewStudent(mockClock, "Bob", "Johnson", nil, 1, 3)
	student3.SetID(3)
	mockRepo.students[3] = student3

	uc := NewStudentUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	students, err := uc.ListByClassID(ctx, 5)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(students) != 2 {
		t.Errorf("expected 2 students, got %d", len(students))
	}

	for _, student := range students {
		if student.ClassID() != 5 {
			t.Errorf("expected ClassID = 5, got %d", student.ClassID())
		}
	}
}
