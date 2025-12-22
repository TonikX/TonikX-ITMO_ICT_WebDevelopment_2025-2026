package handler

import (
	"context"
	"encoding/json"
	"net/http"
	"time"

	"school-service/internal/domain/clock"
	"school-service/internal/domain/health"
	"school-service/internal/domain/logger"
)

const (
	healthCheckTimeout = 5 * time.Second
)

// HealthHandler обработчик для healthcheck
type HealthHandler struct {
	db     health.HealthChecker
	clock  clock.Clock
	logger logger.Logger
}

// writeJSON отправляет JSON ответ
func (h *HealthHandler) writeJSON(w http.ResponseWriter, statusCode int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	if err := json.NewEncoder(w).Encode(v); err != nil {
		h.logger.Error("Failed to encode JSON response", "error", err)
	}
}

// NewHealthHandler создает новый HealthHandler
func NewHealthHandler(db health.HealthChecker, clock clock.Clock, log logger.Logger) *HealthHandler {
	return &HealthHandler{
		db:     db,
		clock:  clock,
		logger: log,
	}
}

// HealthResponse ответ healthcheck
type HealthResponse struct {
	Status    string            `json:"status"`
	Timestamp time.Time         `json:"timestamp"`
	Checks    map[string]string `json:"checks"`
}

// Check обрабатывает запрос на healthcheck
func (h *HealthHandler) Check(w http.ResponseWriter, r *http.Request) {
	ctx, cancel := context.WithTimeout(r.Context(), healthCheckTimeout)
	defer cancel()

	response := HealthResponse{
		Status:    "ok",
		Timestamp: h.clock.Now(),
		Checks:    make(map[string]string),
	}

	if err := h.db.Health(ctx); err != nil {
		response.Status = "unhealthy"
		response.Checks["database"] = "unavailable"
		h.logger.WithError(err).Error("Database health check failed")
	} else {
		response.Checks["database"] = "ok"
	}

	statusCode := http.StatusOK
	if response.Status != "ok" {
		statusCode = http.StatusServiceUnavailable
	}

	h.writeJSON(w, statusCode, response)
}

// Ready обрабатывает запрос на readiness check
func (h *HealthHandler) Ready(w http.ResponseWriter, r *http.Request) {
	ctx, cancel := context.WithTimeout(r.Context(), healthCheckTimeout)
	defer cancel()

	response := HealthResponse{
		Status:    "ready",
		Timestamp: h.clock.Now(),
		Checks:    make(map[string]string),
	}

	if err := h.db.Health(ctx); err != nil {
		response.Status = "not ready"
		response.Checks["database"] = "unavailable"
		h.logger.WithError(err).Error("Database readiness check failed")
		h.writeJSON(w, http.StatusServiceUnavailable, response)
		return
	}

	response.Checks["database"] = "ok"
	h.writeJSON(w, http.StatusOK, response)
}

// Live обрабатывает запрос на liveness check
func (h *HealthHandler) Live(w http.ResponseWriter, r *http.Request) {
	response := HealthResponse{
		Status:    "alive",
		Timestamp: h.clock.Now(),
		Checks:    make(map[string]string),
	}

	h.writeJSON(w, http.StatusOK, response)
}
