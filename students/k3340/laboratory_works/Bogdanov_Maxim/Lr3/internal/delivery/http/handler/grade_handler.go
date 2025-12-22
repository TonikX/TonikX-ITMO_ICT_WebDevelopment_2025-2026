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

// GradeHandler обработчик для работы с оценками
type GradeHandler struct {
	*baseHandler
	usecase usecase.GradeUseCase
}

// NewGradeHandler создает новый GradeHandler
func NewGradeHandler(usecase usecase.GradeUseCase, logger logger.Logger) *GradeHandler {
	return &GradeHandler{
		baseHandler: &baseHandler{logger: logger},
		usecase:     usecase,
	}
}

// CreateGradeRequest запрос на создание оценки
type CreateGradeRequest struct {
	StudentID       int `json:"student_id"`
	SubjectID       int `json:"subject_id"`
	GradingPeriodID int `json:"grading_period_id"`
	Grade           int `json:"grade"`
}

// GradeResponse ответ с данными оценки
type GradeResponse struct {
	ID              int    `json:"id"`
	StudentID       int    `json:"student_id"`
	SubjectID       int    `json:"subject_id"`
	GradingPeriodID int    `json:"grading_period_id"`
	Grade           int    `json:"grade"`
	CreatedAt       string `json:"created_at"`
	UpdatedAt       string `json:"updated_at"`
}

// UpdateGradeRequest запрос на обновление оценки
type UpdateGradeRequest struct {
	StudentID       int `json:"student_id"`
	SubjectID       int `json:"subject_id"`
	GradingPeriodID int `json:"grading_period_id"`
	Grade           int `json:"grade"`
}

// toGradeResponse преобразует domain.Grade в GradeResponse
func toGradeResponse(grade *domain.Grade) GradeResponse {
	return GradeResponse{
		ID:              grade.ID(),
		StudentID:       grade.StudentID(),
		SubjectID:       grade.SubjectID(),
		GradingPeriodID: grade.GradingPeriodID(),
		Grade:           grade.Grade(),
		CreatedAt:       grade.CreatedAt().Format("2006-01-02T15:04:05Z07:00"),
		UpdatedAt:       grade.UpdatedAt().Format("2006-01-02T15:04:05Z07:00"),
	}
}

// Create обрабатывает запрос на создание оценки
// @Summary      Создать оценку
// @Description  Создает новую оценку в системе
// @Tags         grades
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        request body CreateGradeRequest true "Данные оценки"
// @Success      201  {object}  GradeResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Router       /grades [post]
func (h *GradeHandler) Create(w http.ResponseWriter, r *http.Request) {
	var req CreateGradeRequest
	if err := h.decodeJSON(r, &req); err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid request body", err)
		return
	}

	grade, err := h.usecase.Create(r.Context(), req.StudentID, req.SubjectID, req.GradingPeriodID, req.Grade)
	if err != nil {
		h.handleError(w, err)
		return
	}

	if grade == nil {
		h.writeError(w, http.StatusInternalServerError, "grade creation returned nil", errors.New("unexpected nil grade"))
		return
	}

	h.writeJSON(w, http.StatusCreated, toGradeResponse(grade))
}

// GetByID обрабатывает запрос на получение оценки по ID
// @Summary      Получить оценку по ID
// @Description  Возвращает информацию об оценке по её ID
// @Tags         grades
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        id path int true "ID оценки"
// @Success      200  {object}  GradeResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /grades/{id} [get]
func (h *GradeHandler) GetByID(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid grade id", err)
		return
	}

	grade, err := h.usecase.GetByID(r.Context(), id)
	if err != nil {
		h.handleError(w, err)
		return
	}

	if grade == nil {
		h.writeError(w, http.StatusInternalServerError, "grade not found", errors.New("unexpected nil grade"))
		return
	}

	h.writeJSON(w, http.StatusOK, toGradeResponse(grade))
}

// Update обрабатывает запрос на обновление оценки
// @Summary      Обновить оценку
// @Description  Обновляет информацию об оценке
// @Tags         grades
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        id path int true "ID оценки"
// @Param        request body UpdateGradeRequest true "Данные оценки"
// @Success      200  {object}  GradeResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /grades/{id} [put]
func (h *GradeHandler) Update(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid grade id", err)
		return
	}

	var req UpdateGradeRequest
	if err := h.decodeJSON(r, &req); err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid request body", err)
		return
	}

	grade, err := h.usecase.Update(r.Context(), id, req.StudentID, req.SubjectID, req.GradingPeriodID, req.Grade)
	if err != nil {
		h.handleError(w, err)
		return
	}

	if grade == nil {
		h.writeError(w, http.StatusInternalServerError, "grade update returned nil", errors.New("unexpected nil grade"))
		return
	}

	h.writeJSON(w, http.StatusOK, toGradeResponse(grade))
}

// Delete обрабатывает запрос на удаление оценки
// @Summary      Удалить оценку
// @Description  Удаляет оценку из системы
// @Tags         grades
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        id path int true "ID оценки"
// @Success      204
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /grades/{id} [delete]
func (h *GradeHandler) Delete(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid grade id", err)
		return
	}

	if err := h.usecase.Delete(r.Context(), id); err != nil {
		h.handleError(w, err)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

// List обрабатывает запрос на получение списка оценок
// @Summary      Список оценок
// @Description  Возвращает список всех оценок
// @Tags         grades
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Success      200  {array}   GradeResponse
// @Failure      401  {object}  map[string]string
// @Router       /grades [get]
func (h *GradeHandler) List(w http.ResponseWriter, r *http.Request) {
	grades, err := h.usecase.List(r.Context())
	if err != nil {
		h.handleError(w, err)
		return
	}

	response := make([]GradeResponse, 0, len(grades))
	for _, grade := range grades {
		response = append(response, toGradeResponse(grade))
	}

	h.writeJSON(w, http.StatusOK, response)
}

// ListByStudentID обрабатывает запрос на получение оценок ученика
// @Summary      Оценки ученика
// @Description  Возвращает список всех оценок указанного ученика
// @Tags         grades
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        studentId path int true "ID ученика"
// @Success      200  {array}   GradeResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Router       /grades/student/{studentId} [get]
func (h *GradeHandler) ListByStudentID(w http.ResponseWriter, r *http.Request) {
	studentIDStr := chi.URLParam(r, "studentId")
	studentID, err := strconv.Atoi(studentIDStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid student id", err)
		return
	}

	grades, err := h.usecase.ListByStudentID(r.Context(), studentID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	response := make([]GradeResponse, 0, len(grades))
	for _, grade := range grades {
		response = append(response, toGradeResponse(grade))
	}

	h.writeJSON(w, http.StatusOK, response)
}

// ListByClassID обрабатывает запрос на получение оценок всех учеников класса
// @Summary      Оценки класса
// @Description  Возвращает список всех оценок всех учеников указанного класса
// @Tags         grades
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        classId path int true "ID класса"
// @Success      200  {array}   GradeResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Router       /grades/class/{classId} [get]
func (h *GradeHandler) ListByClassID(w http.ResponseWriter, r *http.Request) {
	classIDStr := chi.URLParam(r, "classId")
	classID, err := strconv.Atoi(classIDStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid class id", err)
		return
	}

	grades, err := h.usecase.ListByClassID(r.Context(), classID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	response := make([]GradeResponse, 0, len(grades))
	for _, grade := range grades {
		response = append(response, toGradeResponse(grade))
	}

	h.writeJSON(w, http.StatusOK, response)
}

// ListBySubjectID обрабатывает запрос на получение оценок по предмету
// @Summary      Оценки по предмету
// @Description  Возвращает список всех оценок по указанному предмету
// @Tags         grades
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        subjectId path int true "ID предмета"
// @Success      200  {array}   GradeResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Router       /grades/subject/{subjectId} [get]
func (h *GradeHandler) ListBySubjectID(w http.ResponseWriter, r *http.Request) {
	subjectIDStr := chi.URLParam(r, "subjectId")
	subjectID, err := strconv.Atoi(subjectIDStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid subject id", err)
		return
	}

	grades, err := h.usecase.ListBySubjectID(r.Context(), subjectID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	response := make([]GradeResponse, 0, len(grades))
	for _, grade := range grades {
		response = append(response, toGradeResponse(grade))
	}

	h.writeJSON(w, http.StatusOK, response)
}

// ListByClassAndSubject обрабатывает запрос на получение оценок класса по предмету
// @Summary      Оценки класса по предмету
// @Description  Возвращает список всех оценок указанного класса по указанному предмету
// @Tags         grades
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        classId path int true "ID класса"
// @Param        subjectId path int true "ID предмета"
// @Success      200  {array}   GradeResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Router       /grades/class/{classId}/subject/{subjectId} [get]
func (h *GradeHandler) ListByClassAndSubject(w http.ResponseWriter, r *http.Request) {
	classIDStr := chi.URLParam(r, "classId")
	classID, err := strconv.Atoi(classIDStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid class id", err)
		return
	}

	subjectIDStr := chi.URLParam(r, "subjectId")
	subjectID, err := strconv.Atoi(subjectIDStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid subject id", err)
		return
	}

	grades, err := h.usecase.ListByClassAndSubject(r.Context(), classID, subjectID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	response := make([]GradeResponse, 0, len(grades))
	for _, grade := range grades {
		response = append(response, toGradeResponse(grade))
	}

	h.writeJSON(w, http.StatusOK, response)
}

// ListByClassAndGradingPeriod обрабатывает запрос на получение оценок класса за оценочный период
// @Summary      Оценки класса за период
// @Description  Возвращает список всех оценок указанного класса за указанный оценочный период
// @Tags         grades
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        classId path int true "ID класса"
// @Param        gradingPeriodId path int true "ID оценочного периода"
// @Success      200  {array}   GradeResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Router       /grades/class/{classId}/grading-period/{gradingPeriodId} [get]
func (h *GradeHandler) ListByClassAndGradingPeriod(w http.ResponseWriter, r *http.Request) {
	classIDStr := chi.URLParam(r, "classId")
	classID, err := strconv.Atoi(classIDStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid class id", err)
		return
	}

	gradingPeriodIDStr := chi.URLParam(r, "gradingPeriodId")
	gradingPeriodID, err := strconv.Atoi(gradingPeriodIDStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid grading period id", err)
		return
	}

	grades, err := h.usecase.ListByClassAndGradingPeriod(r.Context(), classID, gradingPeriodID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	response := make([]GradeResponse, 0, len(grades))
	for _, grade := range grades {
		response = append(response, toGradeResponse(grade))
	}

	h.writeJSON(w, http.StatusOK, response)
}
