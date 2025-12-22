package ctx

import (
	"context"
	"testing"
)

func TestGetRequestID(t *testing.T) {
	tests := []struct {
		name      string
		ctx       context.Context
		wantID    string
		wantEmpty bool
	}{
		{
			name:      "context with request ID",
			ctx:       WithRequestIDContext(context.Background(), "test-id-123"),
			wantID:    "test-id-123",
			wantEmpty: false,
		},
		{
			name:      "empty context",
			ctx:       context.Background(),
			wantID:    "",
			wantEmpty: true,
		},
		{
			name:      "context with empty request ID",
			ctx:       WithRequestIDContext(context.Background(), ""),
			wantID:    "",
			wantEmpty: true,
		},
		{
			name:      "nil context",
			ctx:       nil,
			wantID:    "",
			wantEmpty: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			requestID := GetRequestID(tt.ctx)

			if tt.wantEmpty {
				if requestID != "" {
					t.Errorf("expected empty request ID, got: %s", requestID)
				}
			} else {
				if requestID != tt.wantID {
					t.Errorf("expected request ID = %s, got: %s", tt.wantID, requestID)
				}
			}
		})
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
			newCtx := WithRequestIDContext(tt.ctx, tt.requestID)

			if tt.wantEmpty {
				if newCtx != tt.ctx {
					t.Errorf("expected same context for empty request ID")
				}
				return
			}

			if newCtx == nil {
				t.Fatal("expected non-nil context")
			}

			value := GetRequestID(newCtx)
			if value != tt.wantID {
				t.Errorf("expected request ID '%s', got: %s", tt.wantID, value)
			}
		})
	}
}

func TestGetRequestID_WithRequestIDContext(t *testing.T) {
	ctx := context.Background()
	requestID := "test-request-id"

	ctx = WithRequestIDContext(ctx, requestID)
	result := GetRequestID(ctx)

	if result != requestID {
		t.Errorf("expected GetRequestID to return %s, got: %s", requestID, result)
	}
}
