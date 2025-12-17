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

// ClassHandler обработчик для работы с классами
type ClassHandler struct {
	*baseHandler
	usecase usecase.ClassUseCase
}

// NewClassHandler создает новый ClassHandler
func NewClassHandler(usecase usecase.ClassUseCase, logger logger.Logger) *ClassHandler {
	return &ClassHandler{
		baseHandler: &baseHandler{logger: logger},
		usecase:     usecase,
	}
}

// CreateClassRequest запрос на создание класса
type CreateClassRequest struct {
	Grade          int    `json:"grade"`
	Letter         string `json:"letter"`
	AcademicYearID int    `json:"academic_year_id"`
	ClassTeacherID *int   `json:"class_teacher_id,omitempty"`
}

// ClassResponse ответ с данными класса
type ClassResponse struct {
	ID             int    `json:"id"`
	Grade          int    `json:"grade"`
	Letter         string `json:"letter"`
	AcademicYearID int    `json:"academic_year_id"`
	ClassTeacherID *int   `json:"class_teacher_id,omitempty"`
	CreatedAt      string `json:"created_at"`
	UpdatedAt      string `json:"updated_at"`
}

// UpdateClassRequest запрос на обновление класса
type UpdateClassRequest struct {
	Grade          int    `json:"grade"`
	Letter         string `json:"letter"`
	AcademicYearID int    `json:"academic_year_id"`
	ClassTeacherID *int   `json:"class_teacher_id,omitempty"`
}

// toClassResponse преобразует domain.Class в ClassResponse
func toClassResponse(class *domain.Class) ClassResponse {
	return ClassResponse{
		ID:             class.ID(),
		Grade:          class.Grade(),
		Letter:         class.Letter(),
		AcademicYearID: class.AcademicYearID(),
		ClassTeacherID: class.ClassTeacherID(),
		CreatedAt:      class.CreatedAt().Format("2006-01-02T15:04:05Z07:00"),
		UpdatedAt:      class.UpdatedAt().Format("2006-01-02T15:04:05Z07:00"),
	}
}

// Create обрабатывает запрос на создание класса
// @Summary      Создать класс
// @Description  Создает новый класс в системе
// @Tags         classes
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        request body CreateClassRequest true "Данные класса"
// @Success      201  {object}  ClassResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Router       /classes [post]
func (h *ClassHandler) Create(w http.ResponseWriter, r *http.Request) {
	var req CreateClassRequest
	if err := h.decodeJSON(r, &req); err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid request body", err)
		return
	}

	class, err := h.usecase.Create(r.Context(), req.Grade, req.Letter, req.AcademicYearID, req.ClassTeacherID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	if class == nil {
		h.writeError(w, http.StatusInternalServerError, "class creation returned nil", errors.New("unexpected nil class"))
		return
	}

	h.writeJSON(w, http.StatusCreated, toClassResponse(class))
}

// GetByID обрабатывает запрос на получение класса по ID
// @Summary      Получить класс по ID
// @Description  Возвращает информацию о классе по его ID
// @Tags         classes
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        id path int true "ID класса"
// @Success      200  {object}  ClassResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /classes/{id} [get]
func (h *ClassHandler) GetByID(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid class id", err)
		return
	}

	class, err := h.usecase.GetByID(r.Context(), id)
	if err != nil {
		h.handleError(w, err)
		return
	}

	if class == nil {
		h.writeError(w, http.StatusInternalServerError, "class not found", errors.New("unexpected nil class"))
		return
	}

	h.writeJSON(w, http.StatusOK, toClassResponse(class))
}

// Update обрабатывает запрос на обновление класса
// @Summary      Обновить класс
// @Description  Обновляет информацию о классе
// @Tags         classes
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        id path int true "ID класса"
// @Param        request body UpdateClassRequest true "Данные класса"
// @Success      200  {object}  ClassResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /classes/{id} [put]
func (h *ClassHandler) Update(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid class id", err)
		return
	}

	var req UpdateClassRequest
	if err := h.decodeJSON(r, &req); err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid request body", err)
		return
	}

	class, err := h.usecase.Update(r.Context(), id, req.Grade, req.Letter, req.AcademicYearID, req.ClassTeacherID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	if class == nil {
		h.writeError(w, http.StatusInternalServerError, "class update returned nil", errors.New("unexpected nil class"))
		return
	}

	h.writeJSON(w, http.StatusOK, toClassResponse(class))
}

// Delete обрабатывает запрос на удаление класса
// @Summary      Удалить класс
// @Description  Выполняет soft delete класса
// @Tags         classes
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        id path int true "ID класса"
// @Success      204
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /classes/{id} [delete]
func (h *ClassHandler) Delete(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid class id", err)
		return
	}

	if err := h.usecase.Delete(r.Context(), id); err != nil {
		h.handleError(w, err)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

// List обрабатывает запрос на получение списка классов
// @Summary      Список классов
// @Description  Возвращает список всех классов
// @Tags         classes
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Success      200  {array}   ClassResponse
// @Failure      401  {object}  map[string]string
// @Router       /classes [get]
func (h *ClassHandler) List(w http.ResponseWriter, r *http.Request) {
	classes, err := h.usecase.List(r.Context())
	if err != nil {
		h.handleError(w, err)
		return
	}

	response := make([]ClassResponse, 0, len(classes))
	for _, class := range classes {
		response = append(response, toClassResponse(class))
	}

	h.writeJSON(w, http.StatusOK, response)
}

// ListByAcademicYearID обрабатывает запрос на получение списка классов учебного года
// @Summary      Список классов учебного года
// @Description  Возвращает список всех классов указанного учебного года
// @Tags         classes
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        academicYearId path int true "ID учебного года"
// @Success      200  {array}   ClassResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Router       /classes/academic-year/{academicYearId} [get]
func (h *ClassHandler) ListByAcademicYearID(w http.ResponseWriter, r *http.Request) {
	academicYearIDStr := chi.URLParam(r, "academicYearId")
	academicYearID, err := strconv.Atoi(academicYearIDStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid academic year id", err)
		return
	}

	classes, err := h.usecase.ListByAcademicYearID(r.Context(), academicYearID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	response := make([]ClassResponse, 0, len(classes))
	for _, class := range classes {
		response = append(response, toClassResponse(class))
	}

	h.writeJSON(w, http.StatusOK, response)
}
