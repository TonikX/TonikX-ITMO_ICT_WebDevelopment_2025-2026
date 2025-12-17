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

// StudentHandler обработчик для работы с учениками
type StudentHandler struct {
	*baseHandler
	usecase usecase.StudentUseCase
}

// NewStudentHandler создает новый StudentHandler
func NewStudentHandler(usecase usecase.StudentUseCase, logger logger.Logger) *StudentHandler {
	return &StudentHandler{
		baseHandler: &baseHandler{logger: logger},
		usecase:     usecase,
	}
}

// CreateStudentRequest запрос на создание ученика
type CreateStudentRequest struct {
	FirstName  string  `json:"first_name"`
	LastName   string  `json:"last_name"`
	MiddleName *string `json:"middle_name,omitempty"`
	GenderID   int     `json:"gender_id"`
	ClassID    int     `json:"class_id"`
}

// StudentResponse ответ с данными ученика
type StudentResponse struct {
	ID         int     `json:"id"`
	FirstName  string  `json:"first_name"`
	LastName   string  `json:"last_name"`
	MiddleName *string `json:"middle_name,omitempty"`
	GenderID   int     `json:"gender_id"`
	ClassID    int     `json:"class_id"`
	CreatedAt  string  `json:"created_at"`
	UpdatedAt  string  `json:"updated_at"`
}

// UpdateStudentRequest запрос на обновление ученика
type UpdateStudentRequest struct {
	FirstName  string  `json:"first_name"`
	LastName   string  `json:"last_name"`
	MiddleName *string `json:"middle_name,omitempty"`
	GenderID   int     `json:"gender_id"`
	ClassID    int     `json:"class_id"`
}

// toStudentResponse преобразует domain.Student в StudentResponse
func toStudentResponse(student *domain.Student) StudentResponse {
	var middleName *string
	if student.MiddleName() != nil {
		middleName = student.MiddleName()
	}

	return StudentResponse{
		ID:         student.ID(),
		FirstName:  student.FirstName(),
		LastName:   student.LastName(),
		MiddleName: middleName,
		GenderID:   student.GenderID(),
		ClassID:    student.ClassID(),
		CreatedAt:  student.CreatedAt().Format("2006-01-02T15:04:05Z07:00"),
		UpdatedAt:  student.UpdatedAt().Format("2006-01-02T15:04:05Z07:00"),
	}
}

// Create обрабатывает запрос на создание ученика
// @Summary      Создать ученика
// @Description  Создает нового ученика в системе
// @Tags         students
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        request body CreateStudentRequest true "Данные ученика"
// @Success      201  {object}  StudentResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Router       /students [post]
func (h *StudentHandler) Create(w http.ResponseWriter, r *http.Request) {
	var req CreateStudentRequest
	if err := h.decodeJSON(r, &req); err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid request body", err)
		return
	}

	student, err := h.usecase.Create(r.Context(), req.FirstName, req.LastName, req.MiddleName, req.GenderID, req.ClassID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	if student == nil {
		h.writeError(w, http.StatusInternalServerError, "student creation returned nil", errors.New("unexpected nil student"))
		return
	}

	h.writeJSON(w, http.StatusCreated, toStudentResponse(student))
}

// GetByID обрабатывает запрос на получение ученика по ID
// @Summary      Получить ученика по ID
// @Description  Возвращает информацию об ученике по его ID
// @Tags         students
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        id path int true "ID ученика"
// @Success      200  {object}  StudentResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /students/{id} [get]
func (h *StudentHandler) GetByID(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid student id", err)
		return
	}

	student, err := h.usecase.GetByID(r.Context(), id)
	if err != nil {
		h.handleError(w, err)
		return
	}

	if student == nil {
		h.writeError(w, http.StatusInternalServerError, "student not found", errors.New("unexpected nil student"))
		return
	}

	h.writeJSON(w, http.StatusOK, toStudentResponse(student))
}

// Update обрабатывает запрос на обновление ученика
// @Summary      Обновить ученика
// @Description  Обновляет информацию об ученике
// @Tags         students
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        id path int true "ID ученика"
// @Param        request body UpdateStudentRequest true "Данные ученика"
// @Success      200  {object}  StudentResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /students/{id} [put]
func (h *StudentHandler) Update(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid student id", err)
		return
	}

	var req UpdateStudentRequest
	if err := h.decodeJSON(r, &req); err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid request body", err)
		return
	}

	student, err := h.usecase.Update(r.Context(), id, req.FirstName, req.LastName, req.MiddleName, req.GenderID, req.ClassID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	if student == nil {
		h.writeError(w, http.StatusInternalServerError, "student update returned nil", errors.New("unexpected nil student"))
		return
	}

	h.writeJSON(w, http.StatusOK, toStudentResponse(student))
}

// Delete обрабатывает запрос на удаление ученика
// @Summary      Удалить ученика
// @Description  Выполняет soft delete ученика
// @Tags         students
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        id path int true "ID ученика"
// @Success      204
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Failure      404  {object}  map[string]string
// @Router       /students/{id} [delete]
func (h *StudentHandler) Delete(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid student id", err)
		return
	}

	if err := h.usecase.Delete(r.Context(), id); err != nil {
		h.handleError(w, err)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

// List обрабатывает запрос на получение списка учеников
// @Summary      Список учеников
// @Description  Возвращает список всех учеников
// @Tags         students
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Success      200  {array}   StudentResponse
// @Failure      401  {object}  map[string]string
// @Router       /students [get]
func (h *StudentHandler) List(w http.ResponseWriter, r *http.Request) {
	students, err := h.usecase.List(r.Context())
	if err != nil {
		h.handleError(w, err)
		return
	}

	response := make([]StudentResponse, 0, len(students))
	for _, student := range students {
		response = append(response, toStudentResponse(student))
	}

	h.writeJSON(w, http.StatusOK, response)
}

// ListByClassID обрабатывает запрос на получение списка учеников класса
// @Summary      Список учеников класса
// @Description  Возвращает список всех учеников указанного класса
// @Tags         students
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        classId path int true "ID класса"
// @Success      200  {array}   StudentResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Router       /students/class/{classId} [get]
func (h *StudentHandler) ListByClassID(w http.ResponseWriter, r *http.Request) {
	classIDStr := chi.URLParam(r, "classId")
	classID, err := strconv.Atoi(classIDStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid class id", err)
		return
	}

	students, err := h.usecase.ListByClassID(r.Context(), classID)
	if err != nil {
		h.handleError(w, err)
		return
	}

	response := make([]StudentResponse, 0, len(students))
	for _, student := range students {
		response = append(response, toStudentResponse(student))
	}

	h.writeJSON(w, http.StatusOK, response)
}
