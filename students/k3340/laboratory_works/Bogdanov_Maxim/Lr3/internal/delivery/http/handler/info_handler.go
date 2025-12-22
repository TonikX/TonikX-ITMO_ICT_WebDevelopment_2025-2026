package handler

import (
	"net/http"
	"strconv"

	"school-service/internal/domain/logger"
	"school-service/internal/domain/usecase"
)

// InfoHandler обработчик для информационных запросов
type InfoHandler struct {
	baseHandler
	infoUC usecase.InfoUseCase
}

// NewInfoHandler создает новый обработчик информационных запросов
func NewInfoHandler(infoUC usecase.InfoUseCase, logger logger.Logger) *InfoHandler {
	return &InfoHandler{
		baseHandler: baseHandler{logger: logger},
		infoUC:      infoUC,
	}
}

// GetTeachersCountBySubject возвращает количество учителей по каждому предмету
// @Summary      Количество учителей по предметам
// @Description  Возвращает количество учителей, преподающих каждый предмет
// @Tags         info
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Success      200  {object}  map[string]int
// @Failure      401  {object}  map[string]string
// @Router       /info/teachers-count-by-subject [get]
func (h *InfoHandler) GetTeachersCountBySubject(w http.ResponseWriter, r *http.Request) {
	result, err := h.infoUC.GetTeachersCountBySubject(r.Context())
	if err != nil {
		h.handleError(w, err)
		return
	}

	h.writeJSON(w, http.StatusOK, result)
}

// GetTeachersBySameSubjects возвращает учителей, преподающих те же предметы, что и указанный учитель
// @Summary      Учителя с теми же предметами
// @Description  Возвращает список учителей, которые преподают те же предметы, что и указанный учитель
// @Tags         info
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Param        teacherId query int true "ID учителя"
// @Success      200  {array}   TeacherResponse
// @Failure      400  {object}  map[string]string
// @Failure      401  {object}  map[string]string
// @Router       /info/teachers-by-same-subjects [get]
func (h *InfoHandler) GetTeachersBySameSubjects(w http.ResponseWriter, r *http.Request) {
	teacherIDStr := r.URL.Query().Get("teacherId")
	if teacherIDStr == "" {
		h.writeError(w, http.StatusBadRequest, "teacherId parameter is required", nil)
		return
	}

	teacherID, err := strconv.Atoi(teacherIDStr)
	if err != nil {
		h.writeError(w, http.StatusBadRequest, "invalid teacherId parameter", err)
		return
	}

	teachers, err := h.infoUC.GetTeachersBySameSubjects(r.Context(), teacherID)
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

// GetStudentsCountByGender возвращает количество мальчиков и девочек в каждом классе
// @Summary      Количество мальчиков/девочек по классам
// @Description  Возвращает количество мальчиков и девочек в каждом классе
// @Tags         info
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Success      200  {object}  map[int]map[string]int
// @Failure      401  {object}  map[string]string
// @Router       /info/students-count-by-gender [get]
func (h *InfoHandler) GetStudentsCountByGender(w http.ResponseWriter, r *http.Request) {
	result, err := h.infoUC.GetStudentsCountByGender(r.Context())
	if err != nil {
		h.handleError(w, err)
		return
	}

	h.writeJSON(w, http.StatusOK, result)
}

// GetClassroomsCountByType возвращает количество кабинетов базовых и профильных дисциплин
// @Summary      Количество кабинетов по типам
// @Description  Возвращает количество кабинетов для базовых и профильных дисциплин
// @Tags         info
// @Accept       json
// @Produce      json
// @Security     BearerAuth
// @Success      200  {object}  map[string]int
// @Failure      401  {object}  map[string]string
// @Router       /info/classrooms-count-by-type [get]
func (h *InfoHandler) GetClassroomsCountByType(w http.ResponseWriter, r *http.Request) {
	result, err := h.infoUC.GetClassroomsCountByType(r.Context())
	if err != nil {
		h.handleError(w, err)
		return
	}

	h.writeJSON(w, http.StatusOK, result)
}
