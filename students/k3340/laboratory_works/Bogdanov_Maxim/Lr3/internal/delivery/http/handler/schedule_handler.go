package handler

import (
	"errors"
	"net/http"
	"strconv"

	"github.com/go-chi/chi/v5"
	"school-service/internal/domain"
	"school-service/internal/domain/logger"
	"school-service/internal/domain/usecase"
)

// ScheduleHandler обработчик для работы с расписанием
type ScheduleHandler struct {
	*baseHandler
	usecase usecase.ScheduleUseCase
}

// NewScheduleHandler создает новый ScheduleHandler
func NewScheduleHandler(usecase usecase.ScheduleUseCase, logger logger.Logger) *ScheduleHandler {
	return &ScheduleHandler{
		baseHandler: &baseHandler{logger: logger},
		usecase:     usecase,
	}
}

// CreateScheduleRequest запрос на создание записи расписания
type CreateScheduleRequest struct {
	ClassID      int `json:"class_id"`
	WeekdayID    int `json:"weekday_id"`
	LessonNumber int `json:"lesson_number"`
	SubjectID    int `json:"subject_id"`
	TeacherID    int `json:"teacher_id"`
	ClassroomID  int `json:"classroom_id"`
}

// ScheduleResponse ответ с данными расписания
type ScheduleResponse struct {
	ID           int    `json:"id"`
	ClassID      int    `json:"class_id"`
	WeekdayID    int    `json:"weekday_id"`
	LessonNumber int    `json:"lesson_number"`
	SubjectID    int    `json:"subject_id"`
	TeacherID    int    `json:"teacher_id"`
	ClassroomID  int    `json:"classroom_id"`
	CreatedAt    string `json:"created_at"`
	UpdatedAt    string `json:"updated_at"`
}

// UpdateScheduleRequest запрос на обновление записи расписания
type UpdateScheduleRequest struct {
	ClassID      int `json:"class_id"`
	WeekdayID    int `json:"weekday_id"`
	LessonNumber int `json:"lesson_number"`
	SubjectID    int `json:"subject_id"`
	TeacherID    int `json:"teacher_id"`
	ClassroomID  int `json:"classroom_id"`
}

// toScheduleResponse преобразует domain.Schedule в ScheduleResponse
func toScheduleResponse(schedule *domain.Schedule) ScheduleResponse {
	return ScheduleResponse{
		ID:           schedule.ID(),
		ClassID:      schedule.ClassID(),
		WeekdayID:    schedule.WeekdayID(),
		LessonNumber: schedule.LessonNumber(),
		SubjectID:    schedule.SubjectID(),
		TeacherID:    schedule.TeacherID(),
		ClassroomID:  schedule.ClassroomID(),
		CreatedAt:    schedule.CreatedAt().Format("2006-01-02T15:04:05Z07:00"),
		UpdatedAt:    schedule.UpdatedAt().Format("2006-01-02T15:04:05Z07:00"),
	}
}

// Create обрабатывает запрос на создание записи расписания
// @Summary      Создать запись расписания
// @Description  Создает новую запись в расписании
// @Tags         schedules
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        request body CreateScheduleRequest true "Данные расписания"
// @Success      201  {object}  ScheduleResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Router       /schedules [post]
func (h *ScheduleHandler) Create(w http.ResponseWriter, r *http.Request) {
	var req CreateScheduleRequest
	if err := h.decodeJSON(r, &req); err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid request body", err)
		return
	}

	schedule, err := h.usecase.Create(r.Context(), req.ClassID, req.WeekdayID, req.LessonNumber, req.SubjectID, req.TeacherID, req.ClassroomID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	if schedule == nil {
		h.writeError(w, http.StatusInternalServerError, "schedule creation returned nil", errors.New("unexpected nil schedule"))
		return
	}

	h.writeJSON(w, http.StatusCreated, toScheduleResponse(schedule))
}

// GetByID обрабатывает запрос на получение записи расписания по ID
// @Summary      Получить запись расписания по ID
// @Description  Возвращает информацию о записи расписания по её ID
// @Tags         schedules
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        id path int true "ID записи расписания"
// @Success      200  {object}  ScheduleResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /schedules/{id} [get]
func (h *ScheduleHandler) GetByID(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid schedule id", err)
		return
	}

	schedule, err := h.usecase.GetByID(r.Context(), id)
	if err != nil {
		h.handleError(w, err)
		return
	}

	if schedule == nil {
		h.writeError(w, http.StatusInternalServerError, "schedule not found", errors.New("unexpected nil schedule"))
		return
	}

	h.writeJSON(w, http.StatusOK, toScheduleResponse(schedule))
}

// Update обрабатывает запрос на обновление записи расписания
// @Summary      Обновить запись расписания
// @Description  Обновляет информацию о записи расписания
// @Tags         schedules
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        id path int true "ID записи расписания"
// @Param        request body UpdateScheduleRequest true "Данные расписания"
// @Success      200  {object}  ScheduleResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /schedules/{id} [put]
func (h *ScheduleHandler) Update(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid schedule id", err)
		return
	}

	var req UpdateScheduleRequest
	if err := h.decodeJSON(r, &req); err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid request body", err)
		return
	}

	schedule, err := h.usecase.Update(r.Context(), id, req.ClassID, req.WeekdayID, req.LessonNumber, req.SubjectID, req.TeacherID, req.ClassroomID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	if schedule == nil {
		h.writeError(w, http.StatusInternalServerError, "schedule update returned nil", errors.New("unexpected nil schedule"))
		return
	}

	h.writeJSON(w, http.StatusOK, toScheduleResponse(schedule))
}

// Delete обрабатывает запрос на удаление записи расписания
// @Summary      Удалить запись расписания
// @Description  Удаляет запись из расписания
// @Tags         schedules
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        id path int true "ID записи расписания"
// @Success      204
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /schedules/{id} [delete]
func (h *ScheduleHandler) Delete(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid schedule id", err)
		return
	}

	if err := h.usecase.Delete(r.Context(), id); err != nil {
		h.handleError(w, err)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

// List обрабатывает запрос на получение списка записей расписания
// @Summary      Список записей расписания
// @Description  Возвращает список всех записей расписания
// @Tags         schedules
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Success      200  {array}   ScheduleResponse
// @Failure      401  {object}  map[string]string
// @Router       /schedules [get]
func (h *ScheduleHandler) List(w http.ResponseWriter, r *http.Request) {
	schedules, err := h.usecase.List(r.Context())
	if err != nil {
		h.handleError(w, err)
		return
	}

	response := make([]ScheduleResponse, 0, len(schedules))
	for _, schedule := range schedules {
		response = append(response, toScheduleResponse(schedule))
	}

	h.writeJSON(w, http.StatusOK, response)
}

// ListByClassID обрабатывает запрос на получение расписания для класса
// @Summary      Расписание класса
// @Description  Возвращает расписание для указанного класса
// @Tags         schedules
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        classId path int true "ID класса"
// @Success      200  {array}   ScheduleResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Router       /schedules/class/{classId} [get]
func (h *ScheduleHandler) ListByClassID(w http.ResponseWriter, r *http.Request) {
	classIDStr := chi.URLParam(r, "classId")
	classID, err := strconv.Atoi(classIDStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid class id", err)
		return
	}

	schedules, err := h.usecase.ListByClassID(r.Context(), classID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	response := make([]ScheduleResponse, 0, len(schedules))
	for _, schedule := range schedules {
		response = append(response, toScheduleResponse(schedule))
	}

	h.writeJSON(w, http.StatusOK, response)
}

// GetByClassAndWeekdayAndLesson обрабатывает запрос на получение предмета в заданном классе, день недели и номер урока
// @Summary      Предмет в классе на день X урок Y
// @Description  Возвращает предмет, который преподается в указанном классе в указанный день недели на указанном уроке
// @Tags         schedules
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        classId path int true "ID класса"
// @Param        weekdayId path int true "ID дня недели"
// @Param        lessonNumber path int true "Номер урока"
// @Success      200  {object}  ScheduleResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /schedules/class/{classId}/weekday/{weekdayId}/lesson/{lessonNumber} [get]
func (h *ScheduleHandler) GetByClassAndWeekdayAndLesson(w http.ResponseWriter, r *http.Request) {
	classIDStr := chi.URLParam(r, "classId")
	classID, err := strconv.Atoi(classIDStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid class id", err)
		return
	}

	weekdayIDStr := chi.URLParam(r, "weekdayId")
	weekdayID, err := strconv.Atoi(weekdayIDStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid weekday id", err)
		return
	}

	lessonNumberStr := chi.URLParam(r, "lessonNumber")
	lessonNumber, err := strconv.Atoi(lessonNumberStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid lesson number", err)
		return
	}

	schedule, err := h.usecase.GetByClassAndWeekdayAndLesson(r.Context(), classID, weekdayID, lessonNumber)
	if err != nil {
		h.handleError(w, err)
		return
	}

	if schedule == nil {
		h.writeError(w, http.StatusInternalServerError, "schedule not found", errors.New("unexpected nil schedule"))
		return
	}

	h.writeJSON(w, http.StatusOK, toScheduleResponse(schedule))
}
