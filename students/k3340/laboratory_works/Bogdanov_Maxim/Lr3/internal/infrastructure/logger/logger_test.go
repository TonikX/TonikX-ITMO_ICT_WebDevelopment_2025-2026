package logger

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"log/slog"
	"strings"
	"testing"

	ctxkeys "school-service/internal/ctx"
	"school-service/internal/domain"
)

func TestNew(t *testing.T) {
	tests := []struct {
		name      string
		level     string
		format    string
		addSource bool
		logMethod func(*SlogLogger)
		wantLevel string
	}{
		{
			name:      "debug level json format",
			level:     "debug",
			format:    "json",
			addSource: false,
			logMethod: func(l *SlogLogger) { l.Debug("test message") },
			wantLevel: "DEBUG",
		},
		{
			name:      "info level text format",
			level:     "info",
			format:    "text",
			addSource: false,
			logMethod: func(l *SlogLogger) { l.Info("test message") },
			wantLevel: "INFO",
		},
		{
			name:      "warn level with source",
			level:     "warn",
			format:    "json",
			addSource: true,
			logMethod: func(l *SlogLogger) { l.Warn("test message") },
			wantLevel: "WARN",
		},
		{
			name:      "error level",
			level:     "error",
			format:    "json",
			addSource: false,
			logMethod: func(l *SlogLogger) { l.Error("test message") },
			wantLevel: "ERROR",
		},
		{
			name:      "unknown level defaults to info",
			level:     "unknown",
			format:    "json",
			addSource: false,
			logMethod: func(l *SlogLogger) { l.Info("test message") },
			wantLevel: "INFO",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var buf bytes.Buffer
			logger := newLoggerWithBuffer(&buf, tt.level, tt.format, tt.addSource)

			tt.logMethod(logger)

			output := buf.String()
			if output == "" {
				t.Errorf("expected output, got empty string")
				return
			}

			if !strings.Contains(output, tt.wantLevel) && !strings.Contains(output, strings.ToLower(tt.wantLevel)) {
				t.Errorf("expected level %s in output, got: %s", tt.wantLevel, output)
			}
		})
	}
}

func TestDebug(t *testing.T) {
	var buf bytes.Buffer
	logger := newLoggerWithBuffer(&buf, "debug", "json", false)

	logger.Debug("debug message", "key", "value")

	output := buf.String()
	if !strings.Contains(output, "debug message") {
		t.Errorf("expected 'debug message' in output, got: %s", output)
	}
}

func TestInfo(t *testing.T) {
	var buf bytes.Buffer
	logger := newLoggerWithBuffer(&buf, "info", "json", false)

	logger.Info("info message", "key", "value")

	output := buf.String()
	if !strings.Contains(output, "info message") {
		t.Errorf("expected 'info message' in output, got: %s", output)
	}
}

func TestWarn(t *testing.T) {
	var buf bytes.Buffer
	logger := newLoggerWithBuffer(&buf, "warn", "json", false)

	logger.Warn("warn message", "key", "value")

	output := buf.String()
	if !strings.Contains(output, "warn message") {
		t.Errorf("expected 'warn message' in output, got: %s", output)
	}
}

func TestError(t *testing.T) {
	var buf bytes.Buffer
	logger := newLoggerWithBuffer(&buf, "error", "json", false)

	logger.Error("error message", "key", "value")

	output := buf.String()
	if !strings.Contains(output, "error message") {
		t.Errorf("expected 'error message' in output, got: %s", output)
	}
}

func TestWithContext(t *testing.T) {
	tests := []struct {
		name      string
		ctx       context.Context
		wantID    string
		wantEmpty bool
	}{
		{
			name:      "context with request ID",
			ctx:       ctxkeys.WithRequestIDContext(context.Background(), "test-request-id"),
			wantID:    "test-request-id",
			wantEmpty: false,
		},
		{
			name:      "nil context",
			ctx:       nil,
			wantID:    "",
			wantEmpty: true,
		},
		{
			name:      "context without request ID",
			ctx:       context.Background(),
			wantID:    "",
			wantEmpty: true,
		},
		{
			name:      "context with empty request ID",
			ctx:       ctxkeys.WithRequestIDContext(context.Background(), ""),
			wantID:    "",
			wantEmpty: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var buf bytes.Buffer
			logger := newLoggerWithBuffer(&buf, "info", "json", false)

			loggerWithCtx := logger.WithContext(tt.ctx)
			loggerWithCtx.Info("test message")

			output := buf.String()
			if tt.wantEmpty {
				if strings.Contains(output, "request_id") {
					t.Errorf("expected no request_id in output, got: %s", output)
				}
			} else {
				if !strings.Contains(output, tt.wantID) {
					t.Errorf("expected request_id '%s' in output, got: %s", tt.wantID, output)
				}
			}
		})
	}
}

func TestWithRequestID(t *testing.T) {
	tests := []struct {
		name      string
		requestID string
		wantEmpty bool
	}{
		{
			name:      "valid request ID",
			requestID: "test-id-123",
			wantEmpty: false,
		},
		{
			name:      "empty request ID",
			requestID: "",
			wantEmpty: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var buf bytes.Buffer
			logger := newLoggerWithBuffer(&buf, "info", "json", false)

			loggerWithID := logger.WithRequestID(tt.requestID)
			loggerWithID.Info("test message")

			output := buf.String()
			if tt.wantEmpty {
				if strings.Contains(output, "request_id") {
					t.Errorf("expected no request_id in output, got: %s", output)
				}
			} else {
				if !strings.Contains(output, tt.requestID) {
					t.Errorf("expected request_id '%s' in output, got: %s", tt.requestID, output)
				}
			}
		})
	}
}

func TestWithError(t *testing.T) {
	tests := []struct {
		name           string
		err            error
		wantErrorCode  string
		wantEntity     string
		wantField      string
		wantValue      string
		wantReason     string
		wantAdditional bool
	}{
		{
			name:          "domain validation error",
			err:           domain.NewValidationError("teacher", "name", "John", "name is too short"),
			wantErrorCode: "VALIDATION_ERROR",
			wantEntity:    "teacher",
			wantField:     "name",
			wantValue:     "John",
			wantReason:    "name is too short",
		},
		{
			name:          "domain not found error",
			err:           domain.NewNotFoundError("student", "id", 123, "student not found"),
			wantErrorCode: "NOT_FOUND",
			wantEntity:    "student",
			wantField:     "id",
			wantValue:     "123",
			wantReason:    "student not found",
		},
		{
			name:          "regular error",
			err:           errors.New("regular error"),
			wantErrorCode: "",
		},
		{
			name:          "nil error",
			err:           nil,
			wantErrorCode: "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var buf bytes.Buffer
			logger := newLoggerWithBuffer(&buf, "info", "json", false)

			loggerWithErr := logger.WithError(tt.err)
			if tt.err == nil {
				if loggerWithErr != logger {
					t.Errorf("expected same logger instance for nil error")
				}
				return
			}

			loggerWithErr.Info("test message")

			output := buf.String()
			if tt.wantErrorCode != "" {
				if !strings.Contains(output, tt.wantErrorCode) {
					t.Errorf("expected error_code '%s' in output, got: %s", tt.wantErrorCode, output)
				}
			}

			if tt.wantEntity != "" {
				if !strings.Contains(output, tt.wantEntity) {
					t.Errorf("expected entity '%s' in output, got: %s", tt.wantEntity, output)
				}
			}

			if tt.wantField != "" {
				if !strings.Contains(output, tt.wantField) {
					t.Errorf("expected field '%s' in output, got: %s", tt.wantField, output)
				}
			}

			if tt.wantValue != "" {
				if !strings.Contains(output, tt.wantValue) {
					t.Errorf("expected value '%s' in output, got: %s", tt.wantValue, output)
				}
			}

			if tt.wantReason != "" {
				if !strings.Contains(output, tt.wantReason) {
					t.Errorf("expected reason '%s' in output, got: %s", tt.wantReason, output)
				}
			}

			if tt.err != nil && tt.wantErrorCode == "" {
				if !strings.Contains(output, "error") {
					t.Errorf("expected 'error' field in output for regular error, got: %s", output)
				}
			}
		})
	}
}

func TestWithError_DomainErrorWithAdditional(t *testing.T) {
	var buf bytes.Buffer
	logger := newLoggerWithBuffer(&buf, "info", "json", false)

	additional := map[string]any{
		"trace_id": "trace-123",
		"user_id":  456,
	}

	domainErr := &domain.Error{
		Code:       domain.ErrorCodeValidation,
		BaseErr:    domain.ErrValidation,
		Entity:     "teacher",
		Field:      "email",
		Value:      "invalid@",
		Reason:     "invalid email format",
		Additional: additional,
	}

	loggerWithErr := logger.WithError(domainErr)
	loggerWithErr.Info("test message")

	output := buf.String()

	var logEntry map[string]any
	if err := json.Unmarshal([]byte(output), &logEntry); err != nil {
		t.Fatalf("failed to parse JSON output: %v", err)
	}

	if logEntry["trace_id"] != "trace-123" {
		t.Errorf("expected trace_id 'trace-123', got: %v", logEntry["trace_id"])
	}

	if logEntry["user_id"] != float64(456) {
		t.Errorf("expected user_id 456, got: %v", logEntry["user_id"])
	}
}

func TestWithRequestIDContext(t *testing.T) {
	tests := []struct {
		name      string
		ctx       context.Context
		requestID string
		wantID    string
		wantEmpty bool
	}{
		{
			name:      "add request ID to context",
			ctx:       context.Background(),
			requestID: "test-id-456",
			wantID:    "test-id-456",
			wantEmpty: false,
		},
		{
			name:      "empty request ID",
			ctx:       context.Background(),
			requestID: "",
			wantID:    "",
			wantEmpty: true,
		},
		{
			name:      "nil context",
			ctx:       nil,
			requestID: "test-id-789",
			wantID:    "test-id-789",
			wantEmpty: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			newCtx := ctxkeys.WithRequestIDContext(tt.ctx, tt.requestID)

			if tt.wantEmpty {
				if newCtx != tt.ctx {
					t.Errorf("expected same context for empty request ID")
				}
				return
			}

			if newCtx == nil {
				t.Fatal("expected non-nil context")
			}

			value := ctxkeys.GetRequestID(newCtx)
			if value != tt.wantID {
				t.Errorf("expected request ID '%s', got: %v", tt.wantID, value)
			}
		})
	}
}

func TestWithContext_ReturnsSameInstance(t *testing.T) {
	var buf bytes.Buffer
	logger := newLoggerWithBuffer(&buf, "info", "json", false)

	loggerWithNilCtx := logger.WithContext(nil)
	if loggerWithNilCtx != logger {
		t.Errorf("expected same logger instance for nil context")
	}

	loggerWithEmptyCtx := logger.WithContext(context.Background())
	if loggerWithEmptyCtx != logger {
		t.Errorf("expected same logger instance for context without request ID")
	}
}

func TestWithRequestID_ReturnsSameInstance(t *testing.T) {
	var buf bytes.Buffer
	logger := newLoggerWithBuffer(&buf, "info", "json", false)

	loggerWithEmptyID := logger.WithRequestID("")
	if loggerWithEmptyID != logger {
		t.Errorf("expected same logger instance for empty request ID")
	}
}

func TestWithError_ReturnsSameInstance(t *testing.T) {
	var buf bytes.Buffer
	logger := newLoggerWithBuffer(&buf, "info", "json", false)

	loggerWithNilErr := logger.WithError(nil)
	if loggerWithNilErr != logger {
		t.Errorf("expected same logger instance for nil error")
	}
}

func TestLevelFiltering(t *testing.T) {
	tests := []struct {
		name      string
		level     string
		shouldLog map[string]bool
	}{
		{
			name:  "info level",
			level: "info",
			shouldLog: map[string]bool{
				"debug": false,
				"info":  true,
				"warn":  true,
				"error": true,
			},
		},
		{
			name:  "warn level",
			level: "warn",
			shouldLog: map[string]bool{
				"debug": false,
				"info":  false,
				"warn":  true,
				"error": true,
			},
		},
		{
			name:  "error level",
			level: "error",
			shouldLog: map[string]bool{
				"debug": false,
				"info":  false,
				"warn":  false,
				"error": true,
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var buf bytes.Buffer
			logger := newLoggerWithBuffer(&buf, tt.level, "json", false)

			logger.Debug("debug message")
			logger.Info("info message")
			logger.Warn("warn message")
			logger.Error("error message")

			output := buf.String()

			for level, shouldLog := range tt.shouldLog {
				hasLevel := strings.Contains(output, level+" message")
				if shouldLog && !hasLevel {
					t.Errorf("expected %s message to be logged, but it wasn't", level)
				}
				if !shouldLog && hasLevel {
					t.Errorf("expected %s message not to be logged, but it was", level)
				}
			}
		})
	}
}

func newLoggerWithBuffer(buf *bytes.Buffer, level, format string, addSource bool) *SlogLogger {
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
		handler = slog.NewJSONHandler(buf, opts)
	} else {
		handler = slog.NewTextHandler(buf, opts)
	}

	return &SlogLogger{
		logger: slog.New(handler),
	}
}
