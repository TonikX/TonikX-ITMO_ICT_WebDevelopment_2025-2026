package handler

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"school-service/internal/domain"
	"school-service/internal/domain/usecase"
)

type mockReportUseCase struct {
	getClassPerformanceReportErr error
	classPerformanceReport       *usecase.ClassPerformanceReport
}

func newMockReportUseCase() *mockReportUseCase {
	return &mockReportUseCase{
		classPerformanceReport: &usecase.ClassPerformanceReport{
			ClassID:             1,
			ClassName:           "5A",
			StudentsCount:       25,
			OverallAverageGrade: 4.5,
			SubjectPerformance: []usecase.SubjectPerformanceInfo{
				{
					SubjectID:    1,
					SubjectName:  "Math",
					AverageGrade: 4.8,
					GradesCount:  50,
				},
			},
		},
	}
}

func (m *mockReportUseCase) GetClassPerformanceReport(ctx context.Context, classID int) (*usecase.ClassPerformanceReport, error) {
	if m.getClassPerformanceReportErr != nil {
		return nil, m.getClassPerformanceReportErr
	}
	return m.classPerformanceReport, nil
}

func TestReportHandler_GetClassPerformanceReport(t *testing.T) {
	tests := []struct {
		name           string
		classID        string
		setup          func(*mockReportUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockReportUseCase)
	}{
		{
			name:           "successful get",
			classID:        "1",
			setup:          func(m *mockReportUseCase) {},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockReportUseCase) {
				var resp usecase.ClassPerformanceReport
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if resp.ClassID != 1 {
					t.Errorf("expected ClassID 1, got %d", resp.ClassID)
				}
				if resp.StudentsCount != 25 {
					t.Errorf("expected StudentsCount 25, got %d", resp.StudentsCount)
				}
				if len(resp.SubjectPerformance) == 0 {
					t.Error("expected non-empty SubjectPerformance")
				}
			},
		},
		{
			name:           "missing classId",
			classID:        "",
			setup:          func(m *mockReportUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
		{
			name:           "invalid classId",
			classID:        "invalid",
			setup:          func(m *mockReportUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
		{
			name:    "not found",
			classID: "999",
			setup: func(m *mockReportUseCase) {
				m.getClassPerformanceReportErr = domain.NewNotFoundError("Class", "id", 999, "class not found")
			},
			wantStatusCode: http.StatusNotFound,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockReportUseCase()
			tt.setup(mockUC)

			handler := NewReportHandler(mockUC, &mockHandlerLogger{})

			url := "/api/v1/reports/class-performance"
			if tt.classID != "" {
				url += "?classId=" + tt.classID
			}
			req := httptest.NewRequest(http.MethodGet, url, nil)
			w := httptest.NewRecorder()

			handler.GetClassPerformanceReport(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}
