package logger

import "context"

// Logger предоставляет абстракцию для логирования
type Logger interface {
	Debug(msg string, args ...any)
	Info(msg string, args ...any)
	Warn(msg string, args ...any)
	Error(msg string, args ...any)
	WithContext(ctx context.Context) Logger
	WithRequestID(requestID string) Logger
	WithError(err error) Logger
}
