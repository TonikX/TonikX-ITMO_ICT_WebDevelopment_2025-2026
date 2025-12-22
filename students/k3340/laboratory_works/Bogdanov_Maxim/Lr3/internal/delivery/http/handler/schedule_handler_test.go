package handler

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/go-chi/chi/v5"
	"school-service/internal/domain"
	mockclock "school-service/internal/infrastructure/clock"
)

// mockScheduleUseCase мок usecase для расписания
type mockScheduleUseCase struct {
	schedules  map[int]*domain.Schedule
	createErr  error
	getByIDErr error
	updateErr  error
	deleteErr  error
	listErr    error
}

func newMockScheduleUseCase() *mockScheduleUseCase {
	return &mockScheduleUseCase{
		schedules: make(map[int]*domain.Schedule),
	}
}

func (m *mockScheduleUseCase) Create(ctx context.Context, classID, weekdayID, lessonNumber, subjectID, teacherID, classroomID int) (*domain.Schedule, error) {
	if m.createErr != nil {
		return nil, m.createErr
	}
	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	schedule, err := domain.NewSchedule(clock, classID, weekdayID, lessonNumber, subjectID, teacherID, classroomID)
	if err != nil {
		return nil, err
	}
	schedule.SetID(len(m.schedules) + 1)
	m.schedules[schedule.ID()] = schedule
	return schedule, nil
}

func (m *mockScheduleUseCase) GetByID(ctx context.Context, id int) (*domain.Schedule, error) {
	if m.getByIDErr != nil {
		return nil, m.getByIDErr
	}
	schedule, ok := m.schedules[id]
	if !ok {
		return nil, domain.NewNotFoundError("Schedule", "id", id, "schedule not found")
	}
	return schedule, nil
}

func (m *mockScheduleUseCase) Update(ctx context.Context, id int, classID, weekdayID, lessonNumber, subjectID, teacherID, classroomID int) (*domain.Schedule, error) {
	if m.updateErr != nil {
		return nil, m.updateErr
	}
	schedule, ok := m.schedules[id]
	if !ok {
		return nil, domain.NewNotFoundError("Schedule", "id", id, "schedule not found")
	}
	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	schedule.SetClassID(clock, classID)
	schedule.SetWeekdayID(clock, weekdayID)
	schedule.SetLessonNumber(clock, lessonNumber)
	schedule.SetSubjectID(clock, subjectID)
	schedule.SetTeacherID(clock, teacherID)
	schedule.SetClassroomID(clock, classroomID)
	return schedule, nil
}

func (m *mockScheduleUseCase) Delete(ctx context.Context, id int) error {
	if m.deleteErr != nil {
		return m.deleteErr
	}
	if _, ok := m.schedules[id]; !ok {
		return domain.NewNotFoundError("Schedule", "id", id, "schedule not found")
	}
	delete(m.schedules, id)
	return nil
}

func (m *mockScheduleUseCase) List(ctx context.Context) ([]*domain.Schedule, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	schedules := make([]*domain.Schedule, 0, len(m.schedules))
	for _, schedule := range m.schedules {
		schedules = append(schedules, schedule)
	}
	return schedules, nil
}

func (m *mockScheduleUseCase) ListByClassID(ctx context.Context, classID int) ([]*domain.Schedule, error) {
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

func (m *mockScheduleUseCase) GetByClassAndWeekdayAndLesson(ctx context.Context, classID, weekdayID, lessonNumber int) (*domain.Schedule, error) {
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

func TestScheduleHandler_Create(t *testing.T) {
	mockUC := newMockScheduleUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewScheduleHandler(mockUC, mockLog)

	reqBody := map[string]interface{}{
		"class_id":      1,
		"weekday_id":    1,
		"lesson_number": 1,
		"subject_id":    1,
		"teacher_id":    1,
		"classroom_id":  1,
	}
	body, _ := json.Marshal(reqBody)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/schedules", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	handler.Create(w, req)

	if w.Code != http.StatusCreated {
		t.Errorf("expected status %d, got %d", http.StatusCreated, w.Code)
	}

	var response map[string]interface{}
	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Fatalf("failed to unmarshal response: %v", err)
	}

	if response["id"] == nil {
		t.Error("expected id in response")
	}
}

func TestScheduleHandler_Create_InvalidJSON(t *testing.T) {
	mockUC := newMockScheduleUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewScheduleHandler(mockUC, mockLog)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/schedules", bytes.NewReader([]byte("invalid json")))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	handler.Create(w, req)

	if w.Code != http.StatusBadRequest {
		t.Errorf("expected status %d, got %d", http.StatusBadRequest, w.Code)
	}
}

func TestScheduleHandler_GetByID(t *testing.T) {
	mockUC := newMockScheduleUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewScheduleHandler(mockUC, mockLog)

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	schedule, _ := domain.NewSchedule(clock, 1, 1, 1, 1, 1, 1)
	schedule.SetID(1)
	mockUC.schedules[1] = schedule

	req := httptest.NewRequest(http.MethodGet, "/api/v1/schedules/1", nil)
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("id", "1")
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.GetByID(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("expected status %d, got %d", http.StatusOK, w.Code)
	}

	var response map[string]interface{}
	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Fatalf("failed to unmarshal response: %v", err)
	}

	if response["id"].(float64) != 1 {
		t.Errorf("expected id = 1, got %v", response["id"])
	}
}

func TestScheduleHandler_GetByID_NotFound(t *testing.T) {
	mockUC := newMockScheduleUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewScheduleHandler(mockUC, mockLog)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/schedules/999", nil)
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("id", "999")
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.GetByID(w, req)

	if w.Code != http.StatusNotFound {
		t.Errorf("expected status %d, got %d", http.StatusNotFound, w.Code)
	}
}

func TestScheduleHandler_List(t *testing.T) {
	mockUC := newMockScheduleUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewScheduleHandler(mockUC, mockLog)

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	schedule1, _ := domain.NewSchedule(clock, 1, 1, 1, 1, 1, 1)
	schedule1.SetID(1)
	mockUC.schedules[1] = schedule1

	schedule2, _ := domain.NewSchedule(clock, 1, 1, 2, 2, 2, 2)
	schedule2.SetID(2)
	mockUC.schedules[2] = schedule2

	req := httptest.NewRequest(http.MethodGet, "/api/v1/schedules", nil)
	w := httptest.NewRecorder()

	handler.List(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("expected status %d, got %d", http.StatusOK, w.Code)
	}

	var response []map[string]interface{}
	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Fatalf("failed to unmarshal response: %v", err)
	}

	if len(response) != 2 {
		t.Errorf("expected 2 schedules, got %d", len(response))
	}
}

func TestScheduleHandler_Update(t *testing.T) {
	mockUC := newMockScheduleUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewScheduleHandler(mockUC, mockLog)

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	schedule, _ := domain.NewSchedule(clock, 1, 1, 1, 1, 1, 1)
	schedule.SetID(1)
	mockUC.schedules[1] = schedule

	reqBody := map[string]interface{}{
		"class_id":      2,
		"weekday_id":    1,
		"lesson_number": 1,
		"subject_id":    2,
		"teacher_id":    1,
		"classroom_id":  1,
	}
	body, _ := json.Marshal(reqBody)

	req := httptest.NewRequest(http.MethodPut, "/api/v1/schedules/1", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("id", "1")
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.Update(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("expected status %d, got %d", http.StatusOK, w.Code)
	}
}

func TestScheduleHandler_Delete(t *testing.T) {
	mockUC := newMockScheduleUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewScheduleHandler(mockUC, mockLog)

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	schedule, _ := domain.NewSchedule(clock, 1, 1, 1, 1, 1, 1)
	schedule.SetID(1)
	mockUC.schedules[1] = schedule

	req := httptest.NewRequest(http.MethodDelete, "/api/v1/schedules/1", nil)
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("id", "1")
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.Delete(w, req)

	if w.Code != http.StatusNoContent {
		t.Errorf("expected status %d, got %d", http.StatusNoContent, w.Code)
	}
}

func TestScheduleHandler_ListByClassID(t *testing.T) {
	mockUC := newMockScheduleUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewScheduleHandler(mockUC, mockLog)

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	schedule, _ := domain.NewSchedule(clock, 1, 1, 1, 1, 1, 1)
	schedule.SetID(1)
	mockUC.schedules[1] = schedule

	req := httptest.NewRequest(http.MethodGet, "/api/v1/schedules/class/1", nil)
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("classId", "1")
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.ListByClassID(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("expected status %d, got %d", http.StatusOK, w.Code)
	}
}

func TestScheduleHandler_GetByClassAndWeekdayAndLesson(t *testing.T) {
	mockUC := newMockScheduleUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewScheduleHandler(mockUC, mockLog)

	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	schedule, _ := domain.NewSchedule(clock, 1, 1, 1, 1, 1, 1)
	schedule.SetID(1)
	mockUC.schedules[1] = schedule

	req := httptest.NewRequest(http.MethodGet, "/api/v1/schedules/class/1/weekday/1/lesson/1", nil)
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("classId", "1")
	rctx.URLParams.Add("weekdayId", "1")
	rctx.URLParams.Add("lessonNumber", "1")
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.GetByClassAndWeekdayAndLesson(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("expected status %d, got %d", http.StatusOK, w.Code)
	}
}
