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

type mockStudentUseCase struct {
	students         map[int]*domain.Student
	createErr        error
	getByIDErr       error
	updateErr        error
	deleteErr        error
	listErr          error
	listByClassIDErr error
	createCalled     bool
	updateCalled     bool
	deleteCalled     bool
}

func newMockStudentUseCase() *mockStudentUseCase {
	return &mockStudentUseCase{
		students: make(map[int]*domain.Student),
	}
}

func (m *mockStudentUseCase) Create(ctx context.Context, firstName, lastName string, middleName *string, genderID, classID int) (*domain.Student, error) {
	m.createCalled = true
	if m.createErr != nil {
		return nil, m.createErr
	}
	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	student, err := domain.NewStudent(clock, firstName, lastName, middleName, genderID, classID)
	if err != nil {
		return nil, err
	}
	student.SetID(len(m.students) + 1)
	m.students[student.ID()] = student
	return student, nil
}

func (m *mockStudentUseCase) GetByID(ctx context.Context, id int) (*domain.Student, error) {
	if m.getByIDErr != nil {
		return nil, m.getByIDErr
	}
	student, ok := m.students[id]
	if !ok {
		return nil, domain.NewNotFoundError("Student", "id", id, "student not found")
	}
	return student, nil
}

func (m *mockStudentUseCase) Update(ctx context.Context, id int, firstName, lastName string, middleName *string, genderID, classID int) (*domain.Student, error) {
	m.updateCalled = true
	if m.updateErr != nil {
		return nil, m.updateErr
	}
	student, ok := m.students[id]
	if !ok {
		return nil, domain.NewNotFoundError("Student", "id", id, "student not found")
	}
	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	student.SetFirstName(clock, firstName)
	student.SetLastName(clock, lastName)
	student.SetMiddleName(clock, middleName)
	student.SetGenderID(clock, genderID)
	student.SetClassID(clock, classID)
	return student, nil
}

func (m *mockStudentUseCase) Delete(ctx context.Context, id int) error {
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

func (m *mockStudentUseCase) List(ctx context.Context) ([]*domain.Student, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	students := make([]*domain.Student, 0, len(m.students))
	for _, student := range m.students {
		students = append(students, student)
	}
	return students, nil
}

func (m *mockStudentUseCase) ListByClassID(ctx context.Context, classID int) ([]*domain.Student, error) {
	if m.listByClassIDErr != nil {
		return nil, m.listByClassIDErr
	}
	students := make([]*domain.Student, 0)
	for _, student := range m.students {
		if student.ClassID() == classID {
			students = append(students, student)
		}
	}
	return students, nil
}

func TestStudentHandler_Create(t *testing.T) {
	tests := []struct {
		name           string
		body           interface{}
		setup          func(*mockStudentUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockStudentUseCase)
	}{
		{
			name: "successful creation",
			body: CreateStudentRequest{
				FirstName: "John",
				LastName:  "Doe",
				GenderID:  1,
				ClassID:   1,
			},
			setup:          func(m *mockStudentUseCase) {},
			wantStatusCode: http.StatusCreated,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockStudentUseCase) {
				if !m.createCalled {
					t.Error("expected Create to be called")
				}
				var resp StudentResponse
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if resp.FirstName != "John" {
					t.Errorf("expected FirstName John, got %s", resp.FirstName)
				}
			},
		},
		{
			name:           "invalid JSON",
			body:           "invalid json",
			setup:          func(m *mockStudentUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
		{
			name: "validation error",
			body: CreateStudentRequest{
				FirstName: "",
				LastName:  "Doe",
				GenderID:  1,
				ClassID:   1,
			},
			setup: func(m *mockStudentUseCase) {
				m.createErr = domain.NewValidationError("Student", "first_name", "", "first name is required")
			},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockStudentUseCase()
			tt.setup(mockUC)

			handler := NewStudentHandler(mockUC, &mockHandlerLogger{})

			body, err := json.Marshal(tt.body)
			if err != nil {
				t.Fatalf("failed to marshal body: %v", err)
			}

			req := httptest.NewRequest(http.MethodPost, "/api/v1/students", bytes.NewReader(body))
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

func TestStudentHandler_GetByID(t *testing.T) {
	tests := []struct {
		name           string
		id             string
		setup          func(*mockStudentUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockStudentUseCase)
	}{
		{
			name: "successful get",
			id:   "1",
			setup: func(m *mockStudentUseCase) {
				clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
				student, _ := domain.NewStudent(clock, "John", "Doe", nil, 1, 1)
				student.SetID(1)
				m.students[1] = student
			},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockStudentUseCase) {
				var resp StudentResponse
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
			setup: func(m *mockStudentUseCase) {
				m.getByIDErr = domain.NewNotFoundError("Student", "id", 999, "student not found")
			},
			wantStatusCode: http.StatusNotFound,
			wantErr:        true,
		},
		{
			name:           "invalid ID",
			id:             "invalid",
			setup:          func(m *mockStudentUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockStudentUseCase()
			tt.setup(mockUC)

			handler := NewStudentHandler(mockUC, &mockHandlerLogger{})

			req := httptest.NewRequest(http.MethodGet, "/api/v1/students/"+tt.id, nil)
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

func TestStudentHandler_List(t *testing.T) {
	tests := []struct {
		name           string
		setup          func(*mockStudentUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockStudentUseCase)
	}{
		{
			name: "successful list",
			setup: func(m *mockStudentUseCase) {
				clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
				student1, _ := domain.NewStudent(clock, "John", "Doe", nil, 1, 1)
				student1.SetID(1)
				student2, _ := domain.NewStudent(clock, "Jane", "Smith", nil, 2, 1)
				student2.SetID(2)
				m.students[1] = student1
				m.students[2] = student2
			},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockStudentUseCase) {
				var resp []StudentResponse
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if len(resp) != 2 {
					t.Errorf("expected 2 students, got %d", len(resp))
				}
			},
		},
		{
			name:           "empty list",
			setup:          func(m *mockStudentUseCase) {},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockStudentUseCase) {
				var resp []StudentResponse
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if len(resp) != 0 {
					t.Errorf("expected 0 students, got %d", len(resp))
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockStudentUseCase()
			tt.setup(mockUC)

			handler := NewStudentHandler(mockUC, &mockHandlerLogger{})

			req := httptest.NewRequest(http.MethodGet, "/api/v1/students", nil)
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

func TestStudentHandler_Update(t *testing.T) {
	tests := []struct {
		name           string
		id             string
		body           interface{}
		setup          func(*mockStudentUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockStudentUseCase)
	}{
		{
			name: "successful update",
			id:   "1",
			body: UpdateStudentRequest{
				FirstName: "Updated",
				LastName:  "Name",
				GenderID:  1,
				ClassID:   1,
			},
			setup: func(m *mockStudentUseCase) {
				clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
				student, _ := domain.NewStudent(clock, "John", "Doe", nil, 1, 1)
				student.SetID(1)
				m.students[1] = student
			},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockStudentUseCase) {
				if !m.updateCalled {
					t.Error("expected Update to be called")
				}
			},
		},
		{
			name: "not found",
			id:   "999",
			body: UpdateStudentRequest{
				FirstName: "Updated",
				LastName:  "Name",
				GenderID:  1,
				ClassID:   1,
			},
			setup: func(m *mockStudentUseCase) {
				m.updateErr = domain.NewNotFoundError("Student", "id", 999, "student not found")
			},
			wantStatusCode: http.StatusNotFound,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockStudentUseCase()
			tt.setup(mockUC)

			handler := NewStudentHandler(mockUC, &mockHandlerLogger{})

			body, err := json.Marshal(tt.body)
			if err != nil {
				t.Fatalf("failed to marshal body: %v", err)
			}

			req := httptest.NewRequest(http.MethodPut, "/api/v1/students/"+tt.id, bytes.NewReader(body))
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

func TestStudentHandler_Delete(t *testing.T) {
	tests := []struct {
		name           string
		id             string
		setup          func(*mockStudentUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockStudentUseCase)
	}{
		{
			name: "successful delete",
			id:   "1",
			setup: func(m *mockStudentUseCase) {
				clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
				student, _ := domain.NewStudent(clock, "John", "Doe", nil, 1, 1)
				student.SetID(1)
				m.students[1] = student
			},
			wantStatusCode: http.StatusNoContent,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockStudentUseCase) {
				if !m.deleteCalled {
					t.Error("expected Delete to be called")
				}
			},
		},
		{
			name: "not found",
			id:   "999",
			setup: func(m *mockStudentUseCase) {
				m.deleteErr = domain.NewNotFoundError("Student", "id", 999, "student not found")
			},
			wantStatusCode: http.StatusNotFound,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockStudentUseCase()
			tt.setup(mockUC)

			handler := NewStudentHandler(mockUC, &mockHandlerLogger{})

			req := httptest.NewRequest(http.MethodDelete, "/api/v1/students/"+tt.id, nil)
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

func TestStudentHandler_ListByClassID(t *testing.T) {
	tests := []struct {
		name           string
		classID        string
		setup          func(*mockStudentUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockStudentUseCase)
	}{
		{
			name:    "successful list by class",
			classID: "1",
			setup: func(m *mockStudentUseCase) {
				clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
				student1, _ := domain.NewStudent(clock, "John", "Doe", nil, 1, 1)
				student1.SetID(1)
				student2, _ := domain.NewStudent(clock, "Jane", "Smith", nil, 2, 1)
				student2.SetID(2)
				m.students[1] = student1
				m.students[2] = student2
			},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockStudentUseCase) {
				var resp []StudentResponse
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if len(resp) != 2 {
					t.Errorf("expected 2 students, got %d", len(resp))
				}
			},
		},
		{
			name:           "invalid class ID",
			classID:        "invalid",
			setup:          func(m *mockStudentUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockStudentUseCase()
			tt.setup(mockUC)

			handler := NewStudentHandler(mockUC, &mockHandlerLogger{})

			req := httptest.NewRequest(http.MethodGet, "/api/v1/students/class/"+tt.classID, nil)
			rctx := chi.NewRouteContext()
			rctx.URLParams.Add("classId", tt.classID)
			req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
			w := httptest.NewRecorder()

			handler.ListByClassID(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}
