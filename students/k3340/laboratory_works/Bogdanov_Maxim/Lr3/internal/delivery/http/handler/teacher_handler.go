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

// TeacherHandler обработчик для работы с учителями
type TeacherHandler struct {
	*baseHandler
	usecase usecase.TeacherUseCase
}

// NewTeacherHandler создает новый TeacherHandler
func NewTeacherHandler(usecase usecase.TeacherUseCase, logger logger.Logger) *TeacherHandler {
	return &TeacherHandler{
		baseHandler: &baseHandler{logger: logger},
		usecase:     usecase,
	}
}

// CreateTeacherRequest запрос на создание учителя
type CreateTeacherRequest struct {
	FirstName   string  `json:"first_name"`
	LastName    string  `json:"last_name"`
	MiddleName  *string `json:"middle_name,omitempty"`
	ClassroomID *int    `json:"classroom_id,omitempty"`
}

// TeacherResponse ответ с данными учителя
type TeacherResponse struct {
	ID          int     `json:"id"`
	FirstName   string  `json:"first_name"`
	LastName    string  `json:"last_name"`
	MiddleName  *string `json:"middle_name,omitempty"`
	ClassroomID *int    `json:"classroom_id,omitempty"`
	CreatedAt   string  `json:"created_at"`
	UpdatedAt   string  `json:"updated_at"`
}

// UpdateTeacherRequest запрос на обновление учителя
type UpdateTeacherRequest struct {
	FirstName   string  `json:"first_name"`
	LastName    string  `json:"last_name"`
	MiddleName  *string `json:"middle_name,omitempty"`
	ClassroomID *int    `json:"classroom_id,omitempty"`
}

// toTeacherResponse преобразует domain.Teacher в TeacherResponse
func toTeacherResponse(teacher *domain.Teacher) TeacherResponse {
	var middleName *string
	if teacher.MiddleName() != nil {
		middleName = teacher.MiddleName()
	}

	return TeacherResponse{
		ID:          teacher.ID(),
		FirstName:   teacher.FirstName(),
		LastName:    teacher.LastName(),
		MiddleName:  middleName,
		ClassroomID: teacher.ClassroomID(),
		CreatedAt:   teacher.CreatedAt().Format("2006-01-02T15:04:05Z07:00"),
		UpdatedAt:   teacher.UpdatedAt().Format("2006-01-02T15:04:05Z07:00"),
	}
}

// Create обрабатывает запрос на создание учителя
// @Summary      Создать учителя
// @Description  Создает нового учителя в системе
// @Tags         teachers
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        request body CreateTeacherRequest true "Данные учителя"
// @Success      201  {object}  TeacherResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Router       /teachers [post]
func (h *TeacherHandler) Create(w http.ResponseWriter, r *http.Request) {
	var req CreateTeacherRequest
	if err := h.decodeJSON(r, &req); err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid request body", err)
		return
	}

	teacher, err := h.usecase.Create(r.Context(), req.FirstName, req.LastName, req.MiddleName, req.ClassroomID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	if teacher == nil {
		h.writeError(w, http.StatusInternalServerError, "teacher creation returned nil", errors.New("unexpected nil teacher"))
		return
	}

	h.writeJSON(w, http.StatusCreated, toTeacherResponse(teacher))
}

// GetByID обрабатывает запрос на получение учителя по ID
// @Summary      Получить учителя по ID
// @Description  Возвращает информацию об учителе по его ID
// @Tags         teachers
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        id path int true "ID учителя"
// @Success      200  {object}  TeacherResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /teachers/{id} [get]
func (h *TeacherHandler) GetByID(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid teacher id", err)
		return
	}

	teacher, err := h.usecase.GetByID(r.Context(), id)
	if err != nil {
		h.handleError(w, err)
		return
	}

	if teacher == nil {
		h.writeError(w, http.StatusInternalServerError, "teacher not found", errors.New("unexpected nil teacher"))
		return
	}

	h.writeJSON(w, http.StatusOK, toTeacherResponse(teacher))
}

// Update обрабатывает запрос на обновление учителя
// @Summary      Обновить учителя
// @Description  Обновляет информацию об учителе
// @Tags         teachers
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        id path int true "ID учителя"
// @Param        request body UpdateTeacherRequest true "Данные учителя"
// @Success      200  {object}  TeacherResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /teachers/{id} [put]
func (h *TeacherHandler) Update(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid teacher id", err)
		return
	}

	var req UpdateTeacherRequest
	if err := h.decodeJSON(r, &req); err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid request body", err)
		return
	}

	teacher, err := h.usecase.Update(r.Context(), id, req.FirstName, req.LastName, req.MiddleName, req.ClassroomID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	if teacher == nil {
		h.writeError(w, http.StatusInternalServerError, "teacher update returned nil", errors.New("unexpected nil teacher"))
		return
	}

	h.writeJSON(w, http.StatusOK, toTeacherResponse(teacher))
}

// Delete обрабатывает запрос на удаление учителя
// @Summary      Удалить учителя
// @Description  Выполняет soft delete учителя
// @Tags         teachers
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        id path int true "ID учителя"
// @Success      204
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /teachers/{id} [delete]
func (h *TeacherHandler) Delete(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid teacher id", err)
		return
	}

	if err := h.usecase.Delete(r.Context(), id); err != nil {
		h.handleError(w, err)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

// List обрабатывает запрос на получение списка учителей
// @Summary      Список учителей
// @Description  Возвращает список всех учителей
// @Tags         teachers
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Success      200  {array}   TeacherResponse
// @Failure      401  {object}  map[string]string
// @Router       /teachers [get]
func (h *TeacherHandler) List(w http.ResponseWriter, r *http.Request) {
	teachers, err := h.usecase.List(r.Context())
	if err != nil {
		h.handleError(w, err)
		return
	}

	response := make([]TeacherResponse, 0, len(teachers))
	for _, teacher := range teachers {
		response = append(response, toTeacherResponse(teacher))
	}

	h.writeJSON(w, http.StatusOK, response)
}
