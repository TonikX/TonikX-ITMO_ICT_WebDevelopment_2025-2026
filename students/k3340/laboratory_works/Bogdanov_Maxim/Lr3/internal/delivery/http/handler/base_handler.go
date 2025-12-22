package handler

import (
	"encoding/json"
	"errors"
	"io"
	"net/http"

	"school-service/internal/domain"
	"school-service/internal/domain/logger"
)

const (
	maxRequestBodySize = 1 << 20 // 1MB
)

// baseHandler базовый handler с общими методами
type baseHandler struct {
	logger logger.Logger
}

// writeJSON отправляет JSON ответ
func (h *baseHandler) writeJSON(w http.ResponseWriter, statusCode int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	if err := json.NewEncoder(w).Encode(v); err != nil {
		h.logger.Error("Failed to encode JSON response", "error", err)
	}
}

// writeError отправляет ошибку в JSON формате
func (h *baseHandler) writeError(w http.ResponseWriter, statusCode int, message string, err error) {
	h.logger.Error(message, "error", err)

	response := map[string]string{
		"error": message,
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	if encodeErr := json.NewEncoder(w).Encode(response); encodeErr != nil {
		h.logger.Error("Failed to encode error response", "error", encodeErr)
	}
}

// handleError обрабатывает ошибки домена
func (h *baseHandler) handleError(w http.ResponseWriter, err error) {
	var domainErr *domain.Error
	if !errors.As(err, &domainErr) {
		h.writeError(w, http.StatusInternalServerError, "internal server error", err)
		return
	}

	statusCode := http.StatusInternalServerError
	switch domainErr.Code {
	case domain.ErrorCodeNotFound:
		statusCode = http.StatusNotFound
	case domain.ErrorCodeValidation:
		statusCode = http.StatusBadRequest
	case domain.ErrorCodeAlreadyExists:
		statusCode = http.StatusConflict
	case domain.ErrorCodeDeleted:
		statusCode = http.StatusGone
	}

	response := map[string]any{
		"error": domainErr.Error(),
	}
	if domainErr.Field != "" {
		response["field"] = domainErr.Field
	}
	if domainErr.Value != nil {
		response["value"] = domainErr.Value
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	if encodeErr := json.NewEncoder(w).Encode(response); encodeErr != nil {
		h.logger.Error("Failed to encode error response", "error", encodeErr)
	}
}

// decodeJSON декодирует JSON из тела запроса с ограничением размера
func (h *baseHandler) decodeJSON(r *http.Request, v any) error {
	r.Body = http.MaxBytesReader(nil, r.Body, maxRequestBodySize)
	defer func() {
		_ = r.Body.Close()
	}()

	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields()

	if err := decoder.Decode(v); err != nil {
		if err == io.EOF {
			return errors.New("request body is empty")
		}
		return err
	}

	return nil
}
