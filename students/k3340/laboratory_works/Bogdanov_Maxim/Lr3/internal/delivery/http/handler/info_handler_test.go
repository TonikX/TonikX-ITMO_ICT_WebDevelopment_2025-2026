package handler

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"school-service/internal/domain"
	mockclock "school-service/internal/infrastructure/clock"
)

type mockInfoUseCase struct {
	teachersCountBySubjectErr error
	teachersBySameSubjectsErr error
	studentsCountByGenderErr  error
	classroomsCountByTypeErr  error
	teachersCountBySubject    map[string]int
	teachersBySameSubjects    []*domain.Teacher
	studentsCountByGender     map[int]map[string]int
	classroomsCountByType     map[string]int
}

func newMockInfoUseCase() *mockInfoUseCase {
	return &mockInfoUseCase{
		teachersCountBySubject: make(map[string]int),
		teachersBySameSubjects: make([]*domain.Teacher, 0),
		studentsCountByGender:  make(map[int]map[string]int),
		classroomsCountByType:  make(map[string]int),
	}
}

func (m *mockInfoUseCase) GetTeachersCountBySubject(ctx context.Context) (map[string]int, error) {
	if m.teachersCountBySubjectErr != nil {
		return nil, m.teachersCountBySubjectErr
	}
	return m.teachersCountBySubject, nil
}

func (m *mockInfoUseCase) GetTeachersBySameSubjects(ctx context.Context, teacherID int) ([]*domain.Teacher, error) {
	if m.teachersBySameSubjectsErr != nil {
		return nil, m.teachersBySameSubjectsErr
	}
	return m.teachersBySameSubjects, nil
}

func (m *mockInfoUseCase) GetStudentsCountByGender(ctx context.Context) (map[int]map[string]int, error) {
	if m.studentsCountByGenderErr != nil {
		return nil, m.studentsCountByGenderErr
	}
	return m.studentsCountByGender, nil
}

func (m *mockInfoUseCase) GetClassroomsCountByType(ctx context.Context) (map[string]int, error) {
	if m.classroomsCountByTypeErr != nil {
		return nil, m.classroomsCountByTypeErr
	}
	return m.classroomsCountByType, nil
}

func TestInfoHandler_GetTeachersCountBySubject(t *testing.T) {
	tests := []struct {
		name           string
		setup          func(*mockInfoUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockInfoUseCase)
	}{
		{
			name: "successful get",
			setup: func(m *mockInfoUseCase) {
				m.teachersCountBySubject["Math"] = 5
				m.teachersCountBySubject["Physics"] = 3
			},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockInfoUseCase) {
				var resp map[string]int
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if resp["Math"] != 5 {
					t.Errorf("expected Math count 5, got %d", resp["Math"])
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockInfoUseCase()
			tt.setup(mockUC)

			handler := NewInfoHandler(mockUC, &mockHandlerLogger{})

			req := httptest.NewRequest(http.MethodGet, "/api/v1/info/teachers-count-by-subject", nil)
			w := httptest.NewRecorder()

			handler.GetTeachersCountBySubject(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}

func TestInfoHandler_GetTeachersBySameSubjects(t *testing.T) {
	tests := []struct {
		name           string
		teacherID      string
		setup          func(*mockInfoUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockInfoUseCase)
	}{
		{
			name:      "successful get",
			teacherID: "1",
			setup: func(m *mockInfoUseCase) {
				clock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
				teacher, _ := domain.NewTeacher(clock, "John", "Doe", nil, nil)
				teacher.SetID(2)
				m.teachersBySameSubjects = append(m.teachersBySameSubjects, teacher)
			},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockInfoUseCase) {
				var resp []interface{}
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if len(resp) != 1 {
					t.Errorf("expected 1 teacher, got %d", len(resp))
				}
			},
		},
		{
			name:           "missing teacherId",
			teacherID:      "",
			setup:          func(m *mockInfoUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
		{
			name:           "invalid teacherId",
			teacherID:      "invalid",
			setup:          func(m *mockInfoUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockInfoUseCase()
			tt.setup(mockUC)

			handler := NewInfoHandler(mockUC, &mockHandlerLogger{})

			url := "/api/v1/info/teachers-by-same-subjects"
			if tt.teacherID != "" {
				url += "?teacherId=" + tt.teacherID
			}
			req := httptest.NewRequest(http.MethodGet, url, nil)
			w := httptest.NewRecorder()

			handler.GetTeachersBySameSubjects(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}

func TestInfoHandler_GetStudentsCountByGender(t *testing.T) {
	tests := []struct {
		name           string
		setup          func(*mockInfoUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockInfoUseCase)
	}{
		{
			name: "successful get",
			setup: func(m *mockInfoUseCase) {
				m.studentsCountByGender[1] = map[string]int{
					"Male":   10,
					"Female": 12,
				}
			},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockInfoUseCase) {
				var resp map[string]interface{}
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if len(resp) == 0 {
					t.Error("expected non-empty response")
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockInfoUseCase()
			tt.setup(mockUC)

			handler := NewInfoHandler(mockUC, &mockHandlerLogger{})

			req := httptest.NewRequest(http.MethodGet, "/api/v1/info/students-count-by-gender", nil)
			w := httptest.NewRecorder()

			handler.GetStudentsCountByGender(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}

func TestInfoHandler_GetClassroomsCountByType(t *testing.T) {
	tests := []struct {
		name           string
		setup          func(*mockInfoUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockInfoUseCase)
	}{
		{
			name: "successful get",
			setup: func(m *mockInfoUseCase) {
				m.classroomsCountByType["Basic"] = 10
				m.classroomsCountByType["Specialized"] = 5
			},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockInfoUseCase) {
				var resp map[string]int
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if resp["Basic"] != 10 {
					t.Errorf("expected Basic count 10, got %d", resp["Basic"])
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockInfoUseCase()
			tt.setup(mockUC)

			handler := NewInfoHandler(mockUC, &mockHandlerLogger{})

			req := httptest.NewRequest(http.MethodGet, "/api/v1/info/classrooms-count-by-type", nil)
			w := httptest.NewRecorder()

			handler.GetClassroomsCountByType(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}
