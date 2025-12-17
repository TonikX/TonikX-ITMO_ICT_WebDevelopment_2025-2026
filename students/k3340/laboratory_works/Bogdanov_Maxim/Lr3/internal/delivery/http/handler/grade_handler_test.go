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

type mockGradeUseCase struct {
	grades                   map[int]*domain.Grade
	createErr                error
	getByIDErr               error
	updateErr                error
	deleteErr                error
	listErr                  error
	listByStudentIDErr       error
	listByClassIDErr         error
	listBySubjectIDErr       error
	listByClassAndSubjectErr error
	listByClassAndPeriodErr  error
	createCalled             bool
	updateCalled             bool
	deleteCalled             bool
}

func newMockGradeUseCase() *mockGradeUseCase {
	return &mockGradeUseCase{
		grades: make(map[int]*domain.Grade),
	}
}

func (m *mockGradeUseCase) Create(ctx context.Context, studentID, subjectID, gradingPeriodID, grade int) (*domain.Grade, error) {
	m.createCalled = true
	if m.createErr != nil {
		return nil, m.createErr
	}
	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	gradeEntity, err := domain.NewGrade(clock, studentID, subjectID, gradingPeriodID, grade)
	if err != nil {
		return nil, err
	}
	gradeEntity.SetID(len(m.grades) + 1)
	m.grades[gradeEntity.ID()] = gradeEntity
	return gradeEntity, nil
}

func (m *mockGradeUseCase) GetByID(ctx context.Context, id int) (*domain.Grade, error) {
	if m.getByIDErr != nil {
		return nil, m.getByIDErr
	}
	grade, ok := m.grades[id]
	if !ok {
		return nil, domain.NewNotFoundError("Grade", "id", id, "grade not found")
	}
	return grade, nil
}

func (m *mockGradeUseCase) Update(ctx context.Context, id int, studentID, subjectID, gradingPeriodID, grade int) (*domain.Grade, error) {
	m.updateCalled = true
	if m.updateErr != nil {
		return nil, m.updateErr
	}
	gradeEntity, ok := m.grades[id]
	if !ok {
		return nil, domain.NewNotFoundError("Grade", "id", id, "grade not found")
	}
	clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	gradeEntity.SetStudentID(clock, studentID)
	gradeEntity.SetSubjectID(clock, subjectID)
	gradeEntity.SetGradingPeriodID(clock, gradingPeriodID)
	gradeEntity.SetGrade(clock, grade)
	return gradeEntity, nil
}

func (m *mockGradeUseCase) Delete(ctx context.Context, id int) error {
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

func (m *mockGradeUseCase) List(ctx context.Context) ([]*domain.Grade, error) {
	if m.listErr != nil {
		return nil, m.listErr
	}
	grades := make([]*domain.Grade, 0, len(m.grades))
	for _, grade := range m.grades {
		grades = append(grades, grade)
	}
	return grades, nil
}

func (m *mockGradeUseCase) ListByStudentID(ctx context.Context, studentID int) ([]*domain.Grade, error) {
	if m.listByStudentIDErr != nil {
		return nil, m.listByStudentIDErr
	}
	grades := make([]*domain.Grade, 0)
	for _, grade := range m.grades {
		if grade.StudentID() == studentID {
			grades = append(grades, grade)
		}
	}
	return grades, nil
}

func (m *mockGradeUseCase) ListByClassID(ctx context.Context, classID int) ([]*domain.Grade, error) {
	if m.listByClassIDErr != nil {
		return nil, m.listByClassIDErr
	}
	return []*domain.Grade{}, nil
}

func (m *mockGradeUseCase) ListBySubjectID(ctx context.Context, subjectID int) ([]*domain.Grade, error) {
	if m.listBySubjectIDErr != nil {
		return nil, m.listBySubjectIDErr
	}
	grades := make([]*domain.Grade, 0)
	for _, grade := range m.grades {
		if grade.SubjectID() == subjectID {
			grades = append(grades, grade)
		}
	}
	return grades, nil
}

func (m *mockGradeUseCase) ListByClassAndSubject(ctx context.Context, classID, subjectID int) ([]*domain.Grade, error) {
	if m.listByClassAndSubjectErr != nil {
		return nil, m.listByClassAndSubjectErr
	}
	return []*domain.Grade{}, nil
}

func (m *mockGradeUseCase) ListByClassAndGradingPeriod(ctx context.Context, classID, gradingPeriodID int) ([]*domain.Grade, error) {
	if m.listByClassAndPeriodErr != nil {
		return nil, m.listByClassAndPeriodErr
	}
	return []*domain.Grade{}, nil
}

func TestGradeHandler_Create(t *testing.T) {
	tests := []struct {
		name           string
		body           interface{}
		setup          func(*mockGradeUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockGradeUseCase)
	}{
		{
			name: "successful creation",
			body: CreateGradeRequest{
				StudentID:       1,
				SubjectID:       1,
				GradingPeriodID: 1,
				Grade:           5,
			},
			setup:          func(m *mockGradeUseCase) {},
			wantStatusCode: http.StatusCreated,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockGradeUseCase) {
				if !m.createCalled {
					t.Error("expected Create to be called")
				}
				var resp GradeResponse
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
			setup:          func(m *mockGradeUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockGradeUseCase()
			tt.setup(mockUC)

			handler := NewGradeHandler(mockUC, &mockHandlerLogger{})

			body, err := json.Marshal(tt.body)
			if err != nil {
				t.Fatalf("failed to marshal body: %v", err)
			}

			req := httptest.NewRequest(http.MethodPost, "/api/v1/grades", bytes.NewReader(body))
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

func TestGradeHandler_GetByID(t *testing.T) {
	tests := []struct {
		name           string
		id             string
		setup          func(*mockGradeUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockGradeUseCase)
	}{
		{
			name: "successful get",
			id:   "1",
			setup: func(m *mockGradeUseCase) {
				clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
				grade, _ := domain.NewGrade(clock, 1, 1, 1, 5)
				grade.SetID(1)
				m.grades[1] = grade
			},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockGradeUseCase) {
				var resp GradeResponse
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
			setup: func(m *mockGradeUseCase) {
				m.getByIDErr = domain.NewNotFoundError("Grade", "id", 999, "grade not found")
			},
			wantStatusCode: http.StatusNotFound,
			wantErr:        true,
		},
		{
			name:           "invalid ID",
			id:             "invalid",
			setup:          func(m *mockGradeUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockGradeUseCase()
			tt.setup(mockUC)

			handler := NewGradeHandler(mockUC, &mockHandlerLogger{})

			req := httptest.NewRequest(http.MethodGet, "/api/v1/grades/"+tt.id, nil)
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

func TestGradeHandler_ListByStudentID(t *testing.T) {
	tests := []struct {
		name           string
		studentID      string
		setup          func(*mockGradeUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockGradeUseCase)
	}{
		{
			name:      "successful list by student",
			studentID: "1",
			setup: func(m *mockGradeUseCase) {
				clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
				grade1, _ := domain.NewGrade(clock, 1, 1, 1, 5)
				grade1.SetID(1)
				grade2, _ := domain.NewGrade(clock, 1, 2, 1, 4)
				grade2.SetID(2)
				m.grades[1] = grade1
				m.grades[2] = grade2
			},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockGradeUseCase) {
				var resp []GradeResponse
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if len(resp) != 2 {
					t.Errorf("expected 2 grades, got %d", len(resp))
				}
			},
		},
		{
			name:           "invalid student ID",
			studentID:      "invalid",
			setup:          func(m *mockGradeUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockGradeUseCase()
			tt.setup(mockUC)

			handler := NewGradeHandler(mockUC, &mockHandlerLogger{})

			req := httptest.NewRequest(http.MethodGet, "/api/v1/grades/student/"+tt.studentID, nil)
			rctx := chi.NewRouteContext()
			rctx.URLParams.Add("studentId", tt.studentID)
			req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
			w := httptest.NewRecorder()

			handler.ListByStudentID(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}

func TestGradeHandler_Delete(t *testing.T) {
	tests := []struct {
		name           string
		id             string
		setup          func(*mockGradeUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockGradeUseCase)
	}{
		{
			name: "successful delete",
			id:   "1",
			setup: func(m *mockGradeUseCase) {
				clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
				grade, _ := domain.NewGrade(clock, 1, 1, 1, 5)
				grade.SetID(1)
				m.grades[1] = grade
			},
			wantStatusCode: http.StatusNoContent,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockGradeUseCase) {
				if !m.deleteCalled {
					t.Error("expected Delete to be called")
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockGradeUseCase()
			tt.setup(mockUC)

			handler := NewGradeHandler(mockUC, &mockHandlerLogger{})

			req := httptest.NewRequest(http.MethodDelete, "/api/v1/grades/"+tt.id, nil)
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
