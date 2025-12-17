package usecase

import (
	"context"
	"errors"
	"testing"
	"time"

	"school-service/internal/domain"
	"school-service/internal/domain/logger"
	mockclock "school-service/internal/infrastructure/clock"
)

// mockTeacherRepository мок репозитория учителей
type mockTeacherRepository struct {
	teachers     map[int]*domain.Teacher
	createErr    error
	getByIDErr   error
	updateErr    error
	deleteErr    error
	listErr      error
	createCalled bool
	updateCalled bool
	deleteCalled bool
}

func newMockTeacherRepository() *mockTeacherRepository {
	return &mockTeacherRepository{
		teachers: make(map[int]*domain.Teacher),
	}
}

func (m *mockTeacherRepository) Create(ctx context.Context, teacher *domain.Teacher) error {
	m.createCalled = true
	if m.createErr != nil {
		return m.createErr
	}
	teacher.SetID(len(m.teachers) + 1)
	m.teachers[teacher.ID()] = teacher
	return nil
}

func (m *mockTeacherRepository) GetByID(ctx context.Context, id int) (*domain.Teacher, error) {
	if m.getByIDErr != nil {
		return nil, m.getByIDErr
	}
	teacher, ok := m.teachers[id]
	if !ok {
		return nil, domain.NewNotFoundError("Teacher", "id", id, "teacher not found")
	}
	return teacher, nil
}

func (m *mockTeacherRepository) GetByIDActive(ctx context.Context, id int) (*domain.Teacher, error) {
	return m.GetByID(ctx, id)
}

func (m *mockTeacherRepository) Update(ctx context.Context, teacher *domain.Teacher) error {
	m.updateCalled = true
	if m.updateErr != nil {
		return m.updateErr
	}
	if _, ok := m.teachers[teacher.ID()]; !ok {
		return domain.NewNotFoundError("Teacher", "id", teacher.ID(), "teacher not found")
	}
	m.teachers[teacher.ID()] = teacher
	return nil
}

func (m *mockTeacherRepository) Delete(ctx context.Context, id int) error {
	m.deleteCalled = true
	if m.deleteErr != nil {
		return m.deleteErr
	}
	if _, ok := m.teachers[id]; !ok {
		return domain.NewNotFoundError("Teacher", "id", id, "teacher not found")
	}
	delete(m.teachers, id)
	return nil
}

func (m *mockTeacherRepository) List(ctx context.Context) ([]*domain.Teacher, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	teachers := make([]*domain.Teacher, 0, len(m.teachers))
	for _, teacher := range m.teachers {
		teachers = append(teachers, teacher)
	}
	return teachers, nil
}

func (m *mockTeacherRepository) ListActive(ctx context.Context) ([]*domain.Teacher, error) {
	return m.List(ctx)
}

// mockLogger мок логгера
type mockLogger struct{}

func (m *mockLogger) Debug(msg string, args ...any) {}
func (m *mockLogger) Info(msg string, args ...any)  {}
func (m *mockLogger) Warn(msg string, args ...any)  {}
func (m *mockLogger) Error(msg string, args ...any) {}
func (m *mockLogger) WithContext(ctx context.Context) logger.Logger {
	return m
}
func (m *mockLogger) WithRequestID(requestID string) logger.Logger {
	return m
}
func (m *mockLogger) WithError(err error) logger.Logger {
	return m
}

func TestTeacherUseCase_Create(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	uc := NewTeacherUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	teacher, err := uc.Create(ctx, "John", "Doe", nil, nil)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if teacher == nil {
		t.Fatal("expected non-nil teacher")
	}

	if teacher.ID() == 0 {
		t.Error("expected teacher to have ID set")
	}

	if teacher.FirstName() != "John" {
		t.Errorf("expected FirstName = John, got %s", teacher.FirstName())
	}

	if !mockRepo.createCalled {
		t.Error("expected Create to be called on repository")
	}
}

func TestTeacherUseCase_Create_ValidationError(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	uc := NewTeacherUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	teacher, err := uc.Create(ctx, "", "Doe", nil, nil)
	if err == nil {
		t.Error("expected validation error")
	}

	if teacher != nil {
		t.Errorf("expected nil teacher, got %v", teacher)
	}
}

func TestTeacherUseCase_Create_RepositoryError(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockTeacherRepository()
	mockRepo.createErr = errors.New("database error")
	mockLog := &mockLogger{}

	uc := NewTeacherUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	teacher, err := uc.Create(ctx, "John", "Doe", nil, nil)
	if err == nil {
		t.Error("expected error")
	}

	if teacher != nil {
		t.Errorf("expected nil teacher, got %v", teacher)
	}
}

func TestTeacherUseCase_GetByID(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	// Создаем учителя через репозиторий
	existingTeacher, _ := domain.NewTeacher(mockClock, "John", "Doe", nil, nil)
	existingTeacher.SetID(1)
	mockRepo.teachers[1] = existingTeacher

	uc := NewTeacherUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	teacher, err := uc.GetByID(ctx, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if teacher == nil {
		t.Fatal("expected non-nil teacher")
	}

	if teacher.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", teacher.ID())
	}
}

func TestTeacherUseCase_GetByID_NotFound(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	uc := NewTeacherUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	teacher, err := uc.GetByID(ctx, 999)
	if err == nil {
		t.Error("expected error")
	}

	if teacher != nil {
		t.Errorf("expected nil teacher, got %v", teacher)
	}

	var domainErr *domain.Error
	if !errors.As(err, &domainErr) {
		t.Errorf("expected domain.Error, got %T", err)
	}
}

func TestTeacherUseCase_Update(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	// Создаем учителя
	existingTeacher, _ := domain.NewTeacher(mockClock, "John", "Doe", nil, nil)
	existingTeacher.SetID(1)
	mockRepo.teachers[1] = existingTeacher

	uc := NewTeacherUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	teacher, err := uc.Update(ctx, 1, "Jane", "Smith", nil, nil)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if teacher == nil {
		t.Fatal("expected non-nil teacher")
	}

	if teacher.FirstName() != "Jane" {
		t.Errorf("expected FirstName = Jane, got %s", teacher.FirstName())
	}

	if teacher.LastName() != "Smith" {
		t.Errorf("expected LastName = Smith, got %s", teacher.LastName())
	}

	if !mockRepo.updateCalled {
		t.Error("expected Update to be called on repository")
	}
}

func TestTeacherUseCase_Update_NotFound(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	uc := NewTeacherUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	teacher, err := uc.Update(ctx, 999, "Jane", "Smith", nil, nil)
	if err == nil {
		t.Error("expected error")
	}

	if teacher != nil {
		t.Errorf("expected nil teacher, got %v", teacher)
	}
}

func TestTeacherUseCase_Delete(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	// Создаем учителя
	existingTeacher, _ := domain.NewTeacher(mockClock, "John", "Doe", nil, nil)
	existingTeacher.SetID(1)
	mockRepo.teachers[1] = existingTeacher

	uc := NewTeacherUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	err := uc.Delete(ctx, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if !mockRepo.deleteCalled {
		t.Error("expected Delete to be called on repository")
	}
}

func TestTeacherUseCase_Delete_NotFound(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	uc := NewTeacherUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	err := uc.Delete(ctx, 999)
	if err == nil {
		t.Error("expected error")
	}
}

func TestTeacherUseCase_List(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	// Создаем несколько учителей
	teacher1, _ := domain.NewTeacher(mockClock, "John", "Doe", nil, nil)
	teacher1.SetID(1)
	mockRepo.teachers[1] = teacher1

	teacher2, _ := domain.NewTeacher(mockClock, "Jane", "Smith", nil, nil)
	teacher2.SetID(2)
	mockRepo.teachers[2] = teacher2

	uc := NewTeacherUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	teachers, err := uc.List(ctx)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(teachers) != 2 {
		t.Errorf("expected 2 teachers, got %d", len(teachers))
	}
}
