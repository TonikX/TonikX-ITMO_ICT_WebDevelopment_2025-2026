package ctx

import (
	"context"

	"github.com/go-chi/chi/v5/middleware"
)

type Key string

const (
	RequestIDKey Key = "request_id"
	UserIDKey    Key = "user_id"
	UsernameKey  Key = "username"
	UserRoleKey  Key = "user_role"
)

// WithRequestIDContext добавляет request ID в контекст
func WithRequestIDContext(ctx context.Context, requestID string) context.Context {
	if requestID == "" {
		return ctx
	}

	if ctx == nil {
		ctx = context.Background()
	}

	return context.WithValue(ctx, RequestIDKey, requestID)
}

// GetRequestID возвращает request ID из контекста
func GetRequestID(ctx context.Context) string {
	if ctx == nil {
		return ""
	}

	if requestID, ok := ctx.Value(RequestIDKey).(string); ok && requestID != "" {
		return requestID
	}

	if requestID := middleware.GetReqID(ctx); requestID != "" {
		return requestID
	}

	return ""
}
