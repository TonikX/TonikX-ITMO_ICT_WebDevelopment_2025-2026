package usecase

import (
	"context"
	"errors"
	"testing"
	"time"

	"school-service/internal/domain"
	mockclock "school-service/internal/infrastructure/clock"
)

// mockScheduleRepository мок репозитория расписания
type mockScheduleRepository struct {
	schedules    map[int]*domain.Schedule
	createErr    error
	getByIDErr   error
	updateErr    error
	deleteErr    error
	listErr      error
	createCalled bool
	updateCalled bool
	deleteCalled bool
}

func newMockScheduleRepository() *mockScheduleRepository {
	return &mockScheduleRepository{
		schedules: make(map[int]*domain.Schedule),
	}
}

func (m *mockScheduleRepository) Create(ctx context.Context, schedule *domain.Schedule) error {
	m.createCalled = true
	if m.createErr != nil {
		return m.createErr
	}
	schedule.SetID(len(m.schedules) + 1)
	m.schedules[schedule.ID()] = schedule
	return nil
}

func (m *mockScheduleRepository) GetByID(ctx context.Context, id int) (*domain.Schedule, error) {
	if m.getByIDErr != nil {
		return nil, m.getByIDErr
	}
	schedule, ok := m.schedules[id]
	if !ok {
		return nil, domain.NewNotFoundError("Schedule", "id", id, "schedule not found")
	}
	return schedule, nil
}

func (m *mockScheduleRepository) Update(ctx context.Context, schedule *domain.Schedule) error {
	m.updateCalled = true
	if m.updateErr != nil {
		return m.updateErr
	}
	if _, ok := m.schedules[schedule.ID()]; !ok {
		return domain.NewNotFoundError("Schedule", "id", schedule.ID(), "schedule not found")
	}
	m.schedules[schedule.ID()] = schedule
	return nil
}

func (m *mockScheduleRepository) Delete(ctx context.Context, id int) error {
	m.deleteCalled = true
	if m.deleteErr != nil {
		return m.deleteErr
	}
	if _, ok := m.schedules[id]; !ok {
		return domain.NewNotFoundError("Schedule", "id", id, "schedule not found")
	}
	delete(m.schedules, id)
	return nil
}

func (m *mockScheduleRepository) List(ctx context.Context) ([]*domain.Schedule, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	schedules := make([]*domain.Schedule, 0, len(m.schedules))
	for _, schedule := range m.schedules {
		schedules = append(schedules, schedule)
	}
	return schedules, nil
}

func (m *mockScheduleRepository) ListByClassID(ctx context.Context, classID int) ([]*domain.Schedule, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	schedules := make([]*domain.Schedule, 0)
	for _, schedule := range m.schedules {
		if schedule.ClassID() == classID {
			schedules = append(schedules, schedule)
		}
	}
	return schedules, nil
}

func (m *mockScheduleRepository) GetByClassAndWeekdayAndLesson(ctx context.Context, classID, weekdayID, lessonNumber int) (*domain.Schedule, error) {
	if m.getByIDErr != nil {
		return nil, m.getByIDErr
	}
	for _, schedule := range m.schedules {
		if schedule.ClassID() == classID && schedule.WeekdayID() == weekdayID && schedule.LessonNumber() == lessonNumber {
			return schedule, nil
		}
	}
	return nil, domain.NewNotFoundError("Schedule", "classID, weekdayID, lessonNumber", nil, "schedule not found")
}

func TestScheduleUseCase_Create(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockScheduleRepository()
	mockLog := &mockLogger{}

	uc := NewScheduleUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	schedule, err := uc.Create(ctx, 1, 1, 1, 1, 1, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if schedule == nil {
		t.Fatal("expected non-nil schedule")
	}

	if schedule.ID() == 0 {
		t.Error("expected non-zero ID")
	}

	if !mockRepo.createCalled {
		t.Error("expected Create to be called on repository")
	}
}

func TestScheduleUseCase_GetByID(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockScheduleRepository()
	mockLog := &mockLogger{}

	schedule, _ := domain.NewSchedule(mockClock, 1, 1, 1, 1, 1, 1)
	schedule.SetID(1)
	mockRepo.schedules[1] = schedule

	uc := NewScheduleUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	result, err := uc.GetByID(ctx, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if result == nil {
		t.Fatal("expected non-nil schedule")
	}

	if result.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", result.ID())
	}
}

func TestScheduleUseCase_GetByID_NotFound(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockScheduleRepository()
	mockLog := &mockLogger{}

	uc := NewScheduleUseCase(mockRepo, mockClock, mockLog)

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

func TestScheduleUseCase_Update(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockScheduleRepository()
	mockLog := &mockLogger{}

	schedule, _ := domain.NewSchedule(mockClock, 1, 1, 1, 1, 1, 1)
	schedule.SetID(1)
	mockRepo.schedules[1] = schedule

	uc := NewScheduleUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	updated, err := uc.Update(ctx, 1, 2, 1, 1, 2, 1, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if updated.ClassID() != 2 {
		t.Errorf("expected ClassID = 2, got %d", updated.ClassID())
	}

	if !mockRepo.updateCalled {
		t.Error("expected Update to be called on repository")
	}
}

func TestScheduleUseCase_Delete(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockScheduleRepository()
	mockLog := &mockLogger{}

	schedule, _ := domain.NewSchedule(mockClock, 1, 1, 1, 1, 1, 1)
	schedule.SetID(1)
	mockRepo.schedules[1] = schedule

	uc := NewScheduleUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	err := uc.Delete(ctx, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if !mockRepo.deleteCalled {
		t.Error("expected Delete to be called on repository")
	}
}

func TestScheduleUseCase_List(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockScheduleRepository()
	mockLog := &mockLogger{}

	schedule1, _ := domain.NewSchedule(mockClock, 1, 1, 1, 1, 1, 1)
	schedule1.SetID(1)
	mockRepo.schedules[1] = schedule1

	schedule2, _ := domain.NewSchedule(mockClock, 1, 1, 2, 2, 2, 2)
	schedule2.SetID(2)
	mockRepo.schedules[2] = schedule2

	uc := NewScheduleUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	schedules, err := uc.List(ctx)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(schedules) != 2 {
		t.Errorf("expected 2 schedules, got %d", len(schedules))
	}
}

func TestScheduleUseCase_ListByClassID(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockScheduleRepository()
	mockLog := &mockLogger{}

	schedule1, _ := domain.NewSchedule(mockClock, 1, 1, 1, 1, 1, 1)
	schedule1.SetID(1)
	mockRepo.schedules[1] = schedule1

	schedule2, _ := domain.NewSchedule(mockClock, 2, 1, 1, 1, 1, 1)
	schedule2.SetID(2)
	mockRepo.schedules[2] = schedule2

	uc := NewScheduleUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	schedules, err := uc.ListByClassID(ctx, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(schedules) != 1 {
		t.Errorf("expected 1 schedule, got %d", len(schedules))
	}
}

func TestScheduleUseCase_GetByClassAndWeekdayAndLesson(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockRepo := newMockScheduleRepository()
	mockLog := &mockLogger{}

	schedule, _ := domain.NewSchedule(mockClock, 1, 1, 1, 1, 1, 1)
	schedule.SetID(1)
	mockRepo.schedules[1] = schedule

	uc := NewScheduleUseCase(mockRepo, mockClock, mockLog)

	ctx := context.Background()
	result, err := uc.GetByClassAndWeekdayAndLesson(ctx, 1, 1, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if result == nil {
		t.Fatal("expected non-nil schedule")
	}

	if result.ID() != 1 {
		t.Errorf("expected ID = 1, got %d", result.ID())
	}
}
