package logger

import (
	"context"
	"errors"
	"log/slog"
	"os"

	ctxkeys "school-service/internal/ctx"
	"school-service/internal/domain"
	"school-service/internal/domain/logger"
)

const (
	logFormatJSON = "json"
	logLevelDebug = "debug"
	logLevelInfo  = "info"
	logLevelWarn  = "warn"
	logLevelError = "error"
)

var _ logger.Logger = (*SlogLogger)(nil)

// SlogLogger реализация Logger на основе slog
type SlogLogger struct {
	logger *slog.Logger
}

// New создает новый экземпляр логгера
func New(level, format string, addSource bool) *SlogLogger {
	var logLevel slog.Level
	switch level {
	case logLevelDebug:
		logLevel = slog.LevelDebug
	case logLevelInfo:
		logLevel = slog.LevelInfo
	case logLevelWarn:
		logLevel = slog.LevelWarn
	case logLevelError:
		logLevel = slog.LevelError
	default:
		logLevel = slog.LevelInfo
	}

	opts := &slog.HandlerOptions{
		Level:     logLevel,
		AddSource: addSource,
	}

	var handler slog.Handler
	if format == logFormatJSON {
		handler = slog.NewJSONHandler(os.Stdout, opts)
	} else {
		handler = slog.NewTextHandler(os.Stdout, opts)
	}

	return &SlogLogger{
		logger: slog.New(handler),
	}
}

// Debug логирует сообщение уровня debug
func (l *SlogLogger) Debug(msg string, args ...any) {
	l.logger.Debug(msg, args...)
}

// Info логирует сообщение уровня info
func (l *SlogLogger) Info(msg string, args ...any) {
	l.logger.Info(msg, args...)
}

// Warn логирует сообщение уровня warn
func (l *SlogLogger) Warn(msg string, args ...any) {
	l.logger.Warn(msg, args...)
}

// Error логирует сообщение уровня error
func (l *SlogLogger) Error(msg string, args ...any) {
	l.logger.Error(msg, args...)
}

// WithContext возвращает логгер с контекстом
func (l *SlogLogger) WithContext(ctx context.Context) logger.Logger {
	if ctx == nil {
		return l
	}

	requestID := ctxkeys.GetRequestID(ctx)
	if requestID != "" {
		return &SlogLogger{
			logger: l.logger.With("request_id", requestID),
		}
	}

	return l
}

// WithRequestID возвращает логгер с request ID
func (l *SlogLogger) WithRequestID(requestID string) logger.Logger {
	if requestID == "" {
		return l
	}
	return &SlogLogger{
		logger: l.logger.With("request_id", requestID),
	}
}

// WithError возвращает логгер с ошибкой
func (l *SlogLogger) WithError(err error) logger.Logger {
	if err == nil {
		return l
	}

	var domainErr *domain.Error
	if errors.As(err, &domainErr) {
		args := []any{
			"error", err.Error(),
			"error_code", string(domainErr.Code),
		}

		if domainErr.Entity != "" {
			args = append(args, "entity", domainErr.Entity)
		}
		if domainErr.Field != "" {
			args = append(args, "field", domainErr.Field)
		}
		if domainErr.Value != nil {
			args = append(args, "value", domainErr.Value)
		}
		if domainErr.Reason != "" {
			args = append(args, "reason", domainErr.Reason)
		}
		if domainErr.Additional != nil && len(domainErr.Additional) > 0 {
			for k, v := range domainErr.Additional {
				args = append(args, k, v)
			}
		}

		return &SlogLogger{
			logger: l.logger.With(args...),
		}
	}

	return &SlogLogger{
		logger: l.logger.With("error", err),
	}
}
