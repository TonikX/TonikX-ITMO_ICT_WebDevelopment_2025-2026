package handler

import (
	"net/http"
	"strconv"

	"github.com/go-chi/chi/v5"
	"school-service/internal/domain/logger"
	"school-service/internal/domain/usecase"
)

// ReferenceHandler обработчик для справочных данных
type ReferenceHandler struct {
	baseHandler
	referenceUC usecase.ReferenceUseCase
}

// NewReferenceHandler создает новый ReferenceHandler
func NewReferenceHandler(referenceUC usecase.ReferenceUseCase, log logger.Logger) *ReferenceHandler {
	return &ReferenceHandler{
		baseHandler: baseHandler{logger: log},
		referenceUC: referenceUC,
	}
}

// SubjectResponse ответ с данными предмета
type SubjectResponse struct {
	ID            int    `json:"id"`
	Name          string `json:"name"`
	SubjectTypeID int    `json:"subject_type_id"`
	CreatedAt     string `json:"created_at"`
	UpdatedAt     string `json:"updated_at"`
}

// ClassroomResponse ответ с данными кабинета
type ClassroomResponse struct {
	ID            int    `json:"id"`
	RoomNumber    string `json:"room_number"`
	SubjectTypeID int    `json:"subject_type_id"`
	CreatedAt     string `json:"created_at"`
	UpdatedAt     string `json:"updated_at"`
}

// AcademicYearResponse ответ с данными учебного года
type AcademicYearResponse struct {
	ID        int    `json:"id"`
	Name      string `json:"name"`
	StartDate string `json:"start_date"`
	EndDate   string `json:"end_date"`
	IsCurrent bool   `json:"is_current"`
	CreatedAt string `json:"created_at"`
	UpdatedAt string `json:"updated_at"`
}

// GradingPeriodResponse ответ с данными периода оценивания
type GradingPeriodResponse struct {
	ID             int    `json:"id"`
	AcademicYearID int    `json:"academic_year_id"`
	Name           string `json:"name"`
	PeriodOrder    int    `json:"period_order"`
	StartDate      string `json:"start_date"`
	EndDate        string `json:"end_date"`
	CreatedAt      string `json:"created_at"`
	UpdatedAt      string `json:"updated_at"`
}

// WeekdayResponse ответ с данными дня недели
type WeekdayResponse struct {
	ID       int    `json:"id"`
	Name     string `json:"name"`
	DayOrder int    `json:"day_order"`
}

// GetAllSubjects возвращает все предметы
// @Summary      Получить все предметы
// @Description  Возвращает список всех предметов
// @Tags         reference
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Success      200  {array}   SubjectResponse
// @Failure      401  {object}  map[string]string
// @Router       /reference/subjects [get]
func (h *ReferenceHandler) GetAllSubjects(w http.ResponseWriter, r *http.Request) {
	subjects, err := h.referenceUC.GetAllSubjects(r.Context())
	if err != nil {
		h.handleError(w, err)
		return
	}

	// Преобразуем в response формат
	response := make([]SubjectResponse, len(subjects))
	for i, subject := range subjects {
		response[i] = SubjectResponse{
			ID:            subject.ID(),
			Name:          subject.Name(),
			SubjectTypeID: subject.SubjectTypeID(),
			CreatedAt:     subject.CreatedAt().Format("2006-01-02T15:04:05Z07:00"),
			UpdatedAt:     subject.UpdatedAt().Format("2006-01-02T15:04:05Z07:00"),
		}
	}

	h.writeJSON(w, http.StatusOK, response)
}

// GetAllClassrooms возвращает все кабинеты
// @Summary      Получить все кабинеты
// @Description  Возвращает список всех кабинетов
// @Tags         reference
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Success      200  {array}   ClassroomResponse
// @Failure      401  {object}  map[string]string
// @Router       /reference/classrooms [get]
func (h *ReferenceHandler) GetAllClassrooms(w http.ResponseWriter, r *http.Request) {
	classrooms, err := h.referenceUC.GetAllClassrooms(r.Context())
	if err != nil {
		h.handleError(w, err)
		return
	}

	// Преобразуем в response формат
	response := make([]ClassroomResponse, len(classrooms))
	for i, classroom := range classrooms {
		response[i] = ClassroomResponse{
			ID:            classroom.ID(),
			RoomNumber:    classroom.RoomNumber(),
			SubjectTypeID: classroom.SubjectTypeID(),
			CreatedAt:     classroom.CreatedAt().Format("2006-01-02T15:04:05Z07:00"),
			UpdatedAt:     classroom.UpdatedAt().Format("2006-01-02T15:04:05Z07:00"),
		}
	}

	h.writeJSON(w, http.StatusOK, response)
}

// GetAllAcademicYears возвращает все учебные годы
// @Summary      Получить все учебные годы
// @Description  Возвращает список всех учебных годов
// @Tags         reference
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Success      200  {array}   AcademicYearResponse
// @Failure      401  {object}  map[string]string
// @Router       /reference/academic-years [get]
func (h *ReferenceHandler) GetAllAcademicYears(w http.ResponseWriter, r *http.Request) {
	academicYears, err := h.referenceUC.GetAllAcademicYears(r.Context())
	if err != nil {
		h.handleError(w, err)
		return
	}

	// Преобразуем в response формат
	response := make([]AcademicYearResponse, len(academicYears))
	for i, ay := range academicYears {
		response[i] = AcademicYearResponse{
			ID:        ay.ID,
			Name:      ay.Name,
			StartDate: ay.StartDate.Format("2006-01-02"),
			EndDate:   ay.EndDate.Format("2006-01-02"),
			IsCurrent: ay.IsCurrent,
			CreatedAt: ay.CreatedAt.Format("2006-01-02T15:04:05Z07:00"),
			UpdatedAt: ay.UpdatedAt.Format("2006-01-02T15:04:05Z07:00"),
		}
	}

	h.writeJSON(w, http.StatusOK, response)
}

// GetAllGradingPeriods возвращает все периоды оценивания
// @Summary      Получить все периоды оценивания
// @Description  Возвращает список всех периодов оценивания
// @Tags         reference
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Success      200  {array}   GradingPeriodResponse
// @Failure      401  {object}  map[string]string
// @Router       /reference/grading-periods [get]
func (h *ReferenceHandler) GetAllGradingPeriods(w http.ResponseWriter, r *http.Request) {
	gradingPeriods, err := h.referenceUC.GetAllGradingPeriods(r.Context())
	if err != nil {
		h.handleError(w, err)
		return
	}

	// Преобразуем в response формат
	response := make([]GradingPeriodResponse, len(gradingPeriods))
	for i, gp := range gradingPeriods {
		response[i] = GradingPeriodResponse{
			ID:             gp.ID,
			AcademicYearID: gp.AcademicYearID,
			Name:           gp.Name,
			PeriodOrder:    gp.PeriodOrder,
			StartDate:      gp.StartDate.Format("2006-01-02"),
			EndDate:        gp.EndDate.Format("2006-01-02"),
			CreatedAt:      gp.CreatedAt.Format("2006-01-02T15:04:05Z07:00"),
			UpdatedAt:      gp.UpdatedAt.Format("2006-01-02T15:04:05Z07:00"),
		}
	}

	h.writeJSON(w, http.StatusOK, response)
}

// GetGradingPeriodsByAcademicYear возвращает периоды оценивания для учебного года
// @Summary      Получить периоды оценивания по учебному году
// @Description  Возвращает список периодов оценивания для указанного учебного года
// @Tags         reference
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        academicYearId path int true "ID учебного года"
// @Success      200  {array}   GradingPeriodResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Router       /reference/grading-periods/academic-year/{academicYearId} [get]
func (h *ReferenceHandler) GetGradingPeriodsByAcademicYear(w http.ResponseWriter, r *http.Request) {
	academicYearIDStr := chi.URLParam(r, "academicYearId")
	academicYearID, err := strconv.Atoi(academicYearIDStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid academic year id", err)
		return
	}

	gradingPeriods, err := h.referenceUC.GetGradingPeriodsByAcademicYear(r.Context(), academicYearID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	// Преобразуем в response формат
	response := make([]GradingPeriodResponse, len(gradingPeriods))
	for i, gp := range gradingPeriods {
		response[i] = GradingPeriodResponse{
			ID:             gp.ID,
			AcademicYearID: gp.AcademicYearID,
			Name:           gp.Name,
			PeriodOrder:    gp.PeriodOrder,
			StartDate:      gp.StartDate.Format("2006-01-02"),
			EndDate:        gp.EndDate.Format("2006-01-02"),
			CreatedAt:      gp.CreatedAt.Format("2006-01-02T15:04:05Z07:00"),
			UpdatedAt:      gp.UpdatedAt.Format("2006-01-02T15:04:05Z07:00"),
		}
	}

	h.writeJSON(w, http.StatusOK, response)
}

// GetAllWeekdays возвращает все дни недели
// @Summary      Получить все дни недели
// @Description  Возвращает список всех дней недели
// @Tags         reference
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Success      200  {array}   WeekdayResponse
// @Failure      401  {object}  map[string]string
// @Router       /reference/weekdays [get]
func (h *ReferenceHandler) GetAllWeekdays(w http.ResponseWriter, r *http.Request) {
	weekdays, err := h.referenceUC.GetAllWeekdays(r.Context())
	if err != nil {
		h.handleError(w, err)
		return
	}

	// Преобразуем в response формат
	response := make([]WeekdayResponse, len(weekdays))
	for i, wd := range weekdays {
		response[i] = WeekdayResponse{
			ID:       wd.ID,
			Name:     wd.Name,
			DayOrder: wd.DayOrder,
		}
	}

	h.writeJSON(w, http.StatusOK, response)
}
