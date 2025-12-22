package handler

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/go-chi/chi/v5"
	"school-service/internal/domain"
	"school-service/internal/domain/logger"
	mockclock "school-service/internal/infrastructure/clock"
)

// mockTeacherUseCase мок usecase для учителей
type mockTeacherUseCase struct {
	teachers   map[int]*domain.Teacher
	createErr  error
	getByIDErr error
	updateErr  error
	deleteErr  error
	listErr    error
}

func newMockTeacherUseCase() *mockTeacherUseCase {
	return &mockTeacherUseCase{
		teachers: make(map[int]*domain.Teacher),
	}
}

func (m *mockTeacherUseCase) Create(ctx context.Context, firstName, lastName string, middleName *string, classroomID *int) (*domain.Teacher, error) {
	if m.createErr != nil {
		return nil, m.createErr
	}
	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	teacher, err := domain.NewTeacher(clock, firstName, lastName, middleName, classroomID)
	if err != nil {
		return nil, err
	}
	teacher.SetID(len(m.teachers) + 1)
	m.teachers[teacher.ID()] = teacher
	return teacher, nil
}

func (m *mockTeacherUseCase) GetByID(ctx context.Context, id int) (*domain.Teacher, error) {
	if m.getByIDErr != nil {
		return nil, m.getByIDErr
	}
	teacher, ok := m.teachers[id]
	if !ok {
		return nil, domain.NewNotFoundError("Teacher", "id", id, "teacher not found")
	}
	return teacher, nil
}

func (m *mockTeacherUseCase) Update(ctx context.Context, id int, firstName, lastName string, middleName *string, classroomID *int) (*domain.Teacher, error) {
	if m.updateErr != nil {
		return nil, m.updateErr
	}
	teacher, ok := m.teachers[id]
	if !ok {
		return nil, domain.NewNotFoundError("Teacher", "id", id, "teacher not found")
	}
	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	teacher.SetFirstName(clock, firstName)
	teacher.SetLastName(clock, lastName)
	teacher.SetMiddleName(clock, middleName)
	teacher.SetClassroomID(clock, classroomID)
	return teacher, nil
}

func (m *mockTeacherUseCase) Delete(ctx context.Context, id int) error {
	if m.deleteErr != nil {
		return m.deleteErr
	}
	if _, ok := m.teachers[id]; !ok {
		return domain.NewNotFoundError("Teacher", "id", id, "teacher not found")
	}
	delete(m.teachers, id)
	return nil
}

func (m *mockTeacherUseCase) List(ctx context.Context) ([]*domain.Teacher, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	teachers := make([]*domain.Teacher, 0, len(m.teachers))
	for _, teacher := range m.teachers {
		teachers = append(teachers, teacher)
	}
	return teachers, nil
}

// mockHandlerLogger мок логгера для handlers
type mockHandlerLogger struct{}

func (m *mockHandlerLogger) Debug(msg string, args ...any) {}
func (m *mockHandlerLogger) Info(msg string, args ...any)  {}
func (m *mockHandlerLogger) Warn(msg string, args ...any)  {}
func (m *mockHandlerLogger) Error(msg string, args ...any) {}
func (m *mockHandlerLogger) WithContext(ctx context.Context) logger.Logger {
	return m
}
func (m *mockHandlerLogger) WithRequestID(requestID string) logger.Logger {
	return m
}
func (m *mockHandlerLogger) WithError(err error) logger.Logger {
	return m
}

func TestTeacherHandler_Create(t *testing.T) {
	mockUC := newMockTeacherUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewTeacherHandler(mockUC, mockLog)

	reqBody := CreateTeacherRequest{
		FirstName:   "John",
		LastName:    "Doe",
		MiddleName:  nil,
		ClassroomID: nil,
	}
	body, _ := json.Marshal(reqBody)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/teachers", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	handler.Create(w, req)

	if w.Code != http.StatusCreated {
		t.Errorf("expected status %d, got %d", http.StatusCreated, w.Code)
	}

	var response TeacherResponse
	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Fatalf("failed to unmarshal response: %v", err)
	}

	if response.FirstName != "John" {
		t.Errorf("expected FirstName = John, got %s", response.FirstName)
	}

	if response.ID == 0 {
		t.Error("expected ID to be set")
	}
}

func TestTeacherHandler_Create_InvalidJSON(t *testing.T) {
	mockUC := newMockTeacherUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewTeacherHandler(mockUC, mockLog)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/teachers", bytes.NewReader([]byte("invalid json")))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	handler.Create(w, req)

	if w.Code != http.StatusBadRequest {
		t.Errorf("expected status %d, got %d", http.StatusBadRequest, w.Code)
	}
}

func TestTeacherHandler_Create_ValidationError(t *testing.T) {
	mockUC := newMockTeacherUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewTeacherHandler(mockUC, mockLog)

	reqBody := CreateTeacherRequest{
		FirstName:   "", // Пустое имя должно вызвать ошибку валидации
		LastName:    "Doe",
		MiddleName:  nil,
		ClassroomID: nil,
	}
	body, _ := json.Marshal(reqBody)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/teachers", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	handler.Create(w, req)

	if w.Code != http.StatusBadRequest {
		t.Errorf("expected status %d, got %d", http.StatusBadRequest, w.Code)
	}
}

func TestTeacherHandler_GetByID(t *testing.T) {
	mockUC := newMockTeacherUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewTeacherHandler(mockUC, mockLog)

	// Создаем учителя через usecase
	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	teacher, _ := domain.NewTeacher(clock, "John", "Doe", nil, nil)
	teacher.SetID(1)
	mockUC.teachers[1] = teacher

	req := httptest.NewRequest(http.MethodGet, "/api/v1/teachers/1", nil)
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("id", "1")
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.GetByID(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("expected status %d, got %d", http.StatusOK, w.Code)
	}

	var response TeacherResponse
	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Fatalf("failed to unmarshal response: %v", err)
	}

	if response.ID != 1 {
		t.Errorf("expected ID = 1, got %d", response.ID)
	}

	if response.FirstName != "John" {
		t.Errorf("expected FirstName = John, got %s", response.FirstName)
	}
}

func TestTeacherHandler_GetByID_InvalidID(t *testing.T) {
	mockUC := newMockTeacherUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewTeacherHandler(mockUC, mockLog)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/teachers/invalid", nil)
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("id", "invalid")
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.GetByID(w, req)

	if w.Code != http.StatusBadRequest {
		t.Errorf("expected status %d, got %d", http.StatusBadRequest, w.Code)
	}
}

func TestTeacherHandler_GetByID_NotFound(t *testing.T) {
	mockUC := newMockTeacherUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewTeacherHandler(mockUC, mockLog)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/teachers/999", nil)
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("id", "999")
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.GetByID(w, req)

	if w.Code != http.StatusNotFound {
		t.Errorf("expected status %d, got %d", http.StatusNotFound, w.Code)
	}
}

func TestTeacherHandler_Update(t *testing.T) {
	mockUC := newMockTeacherUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewTeacherHandler(mockUC, mockLog)

	// Создаем учителя
	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	teacher, _ := domain.NewTeacher(clock, "John", "Doe", nil, nil)
	teacher.SetID(1)
	mockUC.teachers[1] = teacher

	reqBody := UpdateTeacherRequest{
		FirstName:   "Jane",
		LastName:    "Smith",
		MiddleName:  nil,
		ClassroomID: nil,
	}
	body, _ := json.Marshal(reqBody)

	req := httptest.NewRequest(http.MethodPut, "/api/v1/teachers/1", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("id", "1")
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.Update(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("expected status %d, got %d", http.StatusOK, w.Code)
	}

	var response TeacherResponse
	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Fatalf("failed to unmarshal response: %v", err)
	}

	if response.FirstName != "Jane" {
		t.Errorf("expected FirstName = Jane, got %s", response.FirstName)
	}
}

func TestTeacherHandler_Delete(t *testing.T) {
	mockUC := newMockTeacherUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewTeacherHandler(mockUC, mockLog)

	// Создаем учителя
	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	teacher, _ := domain.NewTeacher(clock, "John", "Doe", nil, nil)
	teacher.SetID(1)
	mockUC.teachers[1] = teacher

	req := httptest.NewRequest(http.MethodDelete, "/api/v1/teachers/1", nil)
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("id", "1")
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.Delete(w, req)

	if w.Code != http.StatusNoContent {
		t.Errorf("expected status %d, got %d", http.StatusNoContent, w.Code)
	}
}

func TestTeacherHandler_List(t *testing.T) {
	mockUC := newMockTeacherUseCase()
	mockLog := &mockHandlerLogger{}
	handler := NewTeacherHandler(mockUC, mockLog)

	// Создаем несколько учителей
	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	teacher1, _ := domain.NewTeacher(clock, "John", "Doe", nil, nil)
	teacher1.SetID(1)
	mockUC.teachers[1] = teacher1

	teacher2, _ := domain.NewTeacher(clock, "Jane", "Smith", nil, nil)
	teacher2.SetID(2)
	mockUC.teachers[2] = teacher2

	req := httptest.NewRequest(http.MethodGet, "/api/v1/teachers", nil)
	w := httptest.NewRecorder()

	handler.List(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("expected status %d, got %d", http.StatusOK, w.Code)
	}

	var response []TeacherResponse
	if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
		t.Fatalf("failed to unmarshal response: %v", err)
	}

	if len(response) != 2 {
		t.Errorf("expected 2 teachers, got %d", len(response))
	}
}

func TestTeacherHandler_HandleError_DomainError(t *testing.T) {
	mockUC := newMockTeacherUseCase()
	mockUC.getByIDErr = domain.NewNotFoundError("Teacher", "id", 999, "teacher not found")
	mockLog := &mockHandlerLogger{}
	handler := NewTeacherHandler(mockUC, mockLog)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/teachers/999", nil)
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("id", "999")
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.GetByID(w, req)

	if w.Code != http.StatusNotFound {
		t.Errorf("expected status %d, got %d", http.StatusNotFound, w.Code)
	}

	var errorResponse map[string]any
	if err := json.Unmarshal(w.Body.Bytes(), &errorResponse); err != nil {
		t.Fatalf("failed to unmarshal error response: %v", err)
	}

	if _, ok := errorResponse["error"]; !ok {
		t.Error("expected error field in response")
	}
}

func TestTeacherHandler_HandleError_GenericError(t *testing.T) {
	mockUC := newMockTeacherUseCase()
	mockUC.getByIDErr = errors.New("database connection failed")
	mockLog := &mockHandlerLogger{}
	handler := NewTeacherHandler(mockUC, mockLog)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/teachers/1", nil)
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("id", "1")
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.GetByID(w, req)

	if w.Code != http.StatusInternalServerError {
		t.Errorf("expected status %d, got %d", http.StatusInternalServerError, w.Code)
	}
}
