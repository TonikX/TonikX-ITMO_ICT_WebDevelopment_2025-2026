package handler

import (
	"net/http"
	"strconv"

	"school-service/internal/domain/logger"
	"school-service/internal/domain/usecase"
)

// ReportHandler обработчик для отчетов
type ReportHandler struct {
	baseHandler
	reportUC usecase.ReportUseCase
}

// NewReportHandler создает новый обработчик отчетов
func NewReportHandler(reportUC usecase.ReportUseCase, logger logger.Logger) *ReportHandler {
	return &ReportHandler{
		baseHandler: baseHandler{logger: logger},
		reportUC:    reportUC,
	}
}

// GetClassPerformanceReport возвращает отчет об успеваемости класса
// @Summary      Отчет об успеваемости класса
// @Description  Возвращает отчет об успеваемости класса, включая средние оценки по предметам, общий средний балл, количество учеников и классного руководителя
// @Tags         reports
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        classId query int true "ID класса"
// @Success      200  {object}  usecase.ClassPerformanceReport
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /reports/class-performance [get]
func (h *ReportHandler) GetClassPerformanceReport(w http.ResponseWriter, r *http.Request) {
	classIDStr := r.URL.Query().Get("classId")
	if classIDStr == "" {
		h.writeError(w, http.StatusBadRequest, "classId parameter is required", nil)
		return
	}

	classID, err := strconv.Atoi(classIDStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid classId parameter", err)
		return
	}

	report, err := h.reportUC.GetClassPerformanceReport(r.Context(), classID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	h.writeJSON(w, http.StatusOK, report)
}
