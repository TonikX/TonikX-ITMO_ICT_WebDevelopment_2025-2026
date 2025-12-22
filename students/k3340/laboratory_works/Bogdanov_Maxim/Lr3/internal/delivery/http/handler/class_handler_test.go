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

type mockClassUseCase struct {
	classes               map[int]*domain.Class
	createErr             error
	getByIDErr            error
	updateErr             error
	deleteErr             error
	listErr               error
	listByAcademicYearErr error
	createCalled          bool
	updateCalled          bool
	deleteCalled          bool
}

func newMockClassUseCase() *mockClassUseCase {
	return &mockClassUseCase{
		classes: make(map[int]*domain.Class),
	}
}

func (m *mockClassUseCase) Create(ctx context.Context, grade int, letter string, academicYearID int, classTeacherID *int) (*domain.Class, error) {
	m.createCalled = true
	if m.createErr != nil {
		return nil, m.createErr
	}
	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	class, err := domain.NewClass(clock, grade, letter, academicYearID, classTeacherID)
	if err != nil {
		return nil, err
	}
	class.SetID(len(m.classes) + 1)
	m.classes[class.ID()] = class
	return class, nil
}

func (m *mockClassUseCase) GetByID(ctx context.Context, id int) (*domain.Class, error) {
	if m.getByIDErr != nil {
		return nil, m.getByIDErr
	}
	class, ok := m.classes[id]
	if !ok {
		return nil, domain.NewNotFoundError("Class", "id", id, "class not found")
	}
	return class, nil
}

func (m *mockClassUseCase) Update(ctx context.Context, id int, grade int, letter string, academicYearID int, classTeacherID *int) (*domain.Class, error) {
	m.updateCalled = true
	if m.updateErr != nil {
		return nil, m.updateErr
	}
	class, ok := m.classes[id]
	if !ok {
		return nil, domain.NewNotFoundError("Class", "id", id, "class not found")
	}
	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	class.SetGrade(clock, grade)
	class.SetLetter(clock, letter)
	class.SetAcademicYearID(clock, academicYearID)
	class.SetClassTeacherID(clock, classTeacherID)
	return class, nil
}

func (m *mockClassUseCase) Delete(ctx context.Context, id int) error {
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

func (m *mockClassUseCase) List(ctx context.Context) ([]*domain.Class, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	classes := make([]*domain.Class, 0, len(m.classes))
	for _, class := range m.classes {
		classes = append(classes, class)
	}
	return classes, nil
}

func (m *mockClassUseCase) ListByAcademicYearID(ctx context.Context, academicYearID int) ([]*domain.Class, error) {
	if m.listByAcademicYearErr != nil {
		return nil, m.listByAcademicYearErr
	}
	classes := make([]*domain.Class, 0)
	for _, class := range m.classes {
		if class.AcademicYearID() == academicYearID {
			classes = append(classes, class)
		}
	}
	return classes, nil
}

func TestClassHandler_Create(t *testing.T) {
	tests := []struct {
		name           string
		body           interface{}
		setup          func(*mockClassUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockClassUseCase)
	}{
		{
			name: "successful creation",
			body: CreateClassRequest{
				Grade:          5,
				Letter:         "A",
				AcademicYearID: 1,
			},
			setup:          func(m *mockClassUseCase) {},
			wantStatusCode: http.StatusCreated,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockClassUseCase) {
				if !m.createCalled {
					t.Error("expected Create to be called")
				}
				var resp ClassResponse
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if resp.Grade != 5 {
					t.Errorf("expected Grade 5, got %d", resp.Grade)
				}
			},
		},
		{
			name:           "invalid JSON",
			body:           "invalid json",
			setup:          func(m *mockClassUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockClassUseCase()
			tt.setup(mockUC)

			handler := NewClassHandler(mockUC, &mockHandlerLogger{})

			body, err := json.Marshal(tt.body)
			if err != nil {
				t.Fatalf("failed to marshal body: %v", err)
			}

			req := httptest.NewRequest(http.MethodPost, "/api/v1/classes", bytes.NewReader(body))
			req.Header.Set("Content-Type", "application/json")
			w := httptest.NewRecorder()

			handler.Create(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}

func TestClassHandler_GetByID(t *testing.T) {
	tests := []struct {
		name           string
		id             string
		setup          func(*mockClassUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockClassUseCase)
	}{
		{
			name: "successful get",
			id:   "1",
			setup: func(m *mockClassUseCase) {
				clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
				class, _ := domain.NewClass(clock, 5, "A", 1, nil)
				class.SetID(1)
				m.classes[1] = class
			},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockClassUseCase) {
				var resp ClassResponse
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if resp.ID != 1 {
					t.Errorf("expected ID 1, got %d", resp.ID)
				}
			},
		},
		{
			name: "not found",
			id:   "999",
			setup: func(m *mockClassUseCase) {
				m.getByIDErr = domain.NewNotFoundError("Class", "id", 999, "class not found")
			},
			wantStatusCode: http.StatusNotFound,
			wantErr:        true,
		},
		{
			name:           "invalid ID",
			id:             "invalid",
			setup:          func(m *mockClassUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockClassUseCase()
			tt.setup(mockUC)

			handler := NewClassHandler(mockUC, &mockHandlerLogger{})

			req := httptest.NewRequest(http.MethodGet, "/api/v1/classes/"+tt.id, nil)
			rctx := chi.NewRouteContext()
			rctx.URLParams.Add("id", tt.id)
			req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
			w := httptest.NewRecorder()

			handler.GetByID(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}

func TestClassHandler_List(t *testing.T) {
	tests := []struct {
		name           string
		setup          func(*mockClassUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockClassUseCase)
	}{
		{
			name: "successful list",
			setup: func(m *mockClassUseCase) {
				clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
				class1, _ := domain.NewClass(clock, 5, "A", 1, nil)
				class1.SetID(1)
				class2, _ := domain.NewClass(clock, 6, "B", 1, nil)
				class2.SetID(2)
				m.classes[1] = class1
				m.classes[2] = class2
			},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockClassUseCase) {
				var resp []ClassResponse
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if len(resp) != 2 {
					t.Errorf("expected 2 classes, got %d", len(resp))
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockClassUseCase()
			tt.setup(mockUC)

			handler := NewClassHandler(mockUC, &mockHandlerLogger{})

			req := httptest.NewRequest(http.MethodGet, "/api/v1/classes", nil)
			w := httptest.NewRecorder()

			handler.List(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}

func TestClassHandler_Update(t *testing.T) {
	tests := []struct {
		name           string
		id             string
		body           interface{}
		setup          func(*mockClassUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockClassUseCase)
	}{
		{
			name: "successful update",
			id:   "1",
			body: UpdateClassRequest{
				Grade:          6,
				Letter:         "B",
				AcademicYearID: 1,
			},
			setup: func(m *mockClassUseCase) {
				clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
				class, _ := domain.NewClass(clock, 5, "A", 1, nil)
				class.SetID(1)
				m.classes[1] = class
			},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockClassUseCase) {
				if !m.updateCalled {
					t.Error("expected Update to be called")
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockClassUseCase()
			tt.setup(mockUC)

			handler := NewClassHandler(mockUC, &mockHandlerLogger{})

			body, err := json.Marshal(tt.body)
			if err != nil {
				t.Fatalf("failed to marshal body: %v", err)
			}

			req := httptest.NewRequest(http.MethodPut, "/api/v1/classes/"+tt.id, bytes.NewReader(body))
			req.Header.Set("Content-Type", "application/json")
			rctx := chi.NewRouteContext()
			rctx.URLParams.Add("id", tt.id)
			req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
			w := httptest.NewRecorder()

			handler.Update(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}

func TestClassHandler_Delete(t *testing.T) {
	tests := []struct {
		name           string
		id             string
		setup          func(*mockClassUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockClassUseCase)
	}{
		{
			name: "successful delete",
			id:   "1",
			setup: func(m *mockClassUseCase) {
				clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
				class, _ := domain.NewClass(clock, 5, "A", 1, nil)
				class.SetID(1)
				m.classes[1] = class
			},
			wantStatusCode: http.StatusNoContent,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockClassUseCase) {
				if !m.deleteCalled {
					t.Error("expected Delete to be called")
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockClassUseCase()
			tt.setup(mockUC)

			handler := NewClassHandler(mockUC, &mockHandlerLogger{})

			req := httptest.NewRequest(http.MethodDelete, "/api/v1/classes/"+tt.id, nil)
			rctx := chi.NewRouteContext()
			rctx.URLParams.Add("id", tt.id)
			req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
			w := httptest.NewRecorder()

			handler.Delete(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}

func TestClassHandler_ListByAcademicYearID(t *testing.T) {
	tests := []struct {
		name           string
		academicYearID string
		setup          func(*mockClassUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockClassUseCase)
	}{
		{
			name:           "successful list by academic year",
			academicYearID: "1",
			setup: func(m *mockClassUseCase) {
				clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
				class1, _ := domain.NewClass(clock, 5, "A", 1, nil)
				class1.SetID(1)
				class2, _ := domain.NewClass(clock, 6, "B", 1, nil)
				class2.SetID(2)
				m.classes[1] = class1
				m.classes[2] = class2
			},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockClassUseCase) {
				var resp []ClassResponse
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if len(resp) != 2 {
					t.Errorf("expected 2 classes, got %d", len(resp))
				}
			},
		},
		{
			name:           "invalid academic year ID",
			academicYearID: "invalid",
			setup:          func(m *mockClassUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockClassUseCase()
			tt.setup(mockUC)

			handler := NewClassHandler(mockUC, &mockHandlerLogger{})

			req := httptest.NewRequest(http.MethodGet, "/api/v1/classes/academic-year/"+tt.academicYearID, nil)
			rctx := chi.NewRouteContext()
			rctx.URLParams.Add("academicYearId", tt.academicYearID)
			req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
			w := httptest.NewRecorder()

			handler.ListByAcademicYearID(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}
