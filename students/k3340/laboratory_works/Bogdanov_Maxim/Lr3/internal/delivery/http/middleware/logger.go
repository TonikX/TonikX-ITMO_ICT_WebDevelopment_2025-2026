package middleware

import (
	"net/http"

	"github.com/go-chi/chi/v5/middleware"
	ctxkeys "school-service/internal/ctx"
	"school-service/internal/domain/clock"
	domainlogger "school-service/internal/domain/logger"
)

// LoggerMiddleware логирует HTTP запросы
func LoggerMiddleware(log domainlogger.Logger, clock clock.Clock) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			start := clock.Now()

			requestID := middleware.GetReqID(r.Context())

			ctx := r.Context()
			if requestID != "" {
				ctx = ctxkeys.WithRequestIDContext(ctx, requestID)
				r = r.WithContext(ctx)
			}

			ww := &responseWriter{ResponseWriter: w, statusCode: http.StatusOK}

			next.ServeHTTP(ww, r)

			duration := clock.Since(start)

			log.WithContext(ctx).Info("HTTP request",
				"method", r.Method,
				"path", r.URL.Path,
				"query", r.URL.RawQuery,
				"status", ww.statusCode,
				"duration_ms", duration.Milliseconds(),
				"remote_addr", r.RemoteAddr,
			)
		})
	}
}

type responseWriter struct {
	http.ResponseWriter
	statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
	rw.statusCode = code
	rw.ResponseWriter.WriteHeader(code)
}
