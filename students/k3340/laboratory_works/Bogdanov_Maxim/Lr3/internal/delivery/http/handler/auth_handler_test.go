package handler

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"school-service/internal/domain"
	"school-service/internal/domain/logger"
	"school-service/internal/domain/usecase"
)

type mockAuthUseCase struct {
	registerErr        error
	loginErr           error
	refreshTokenErr    error
	logoutErr          error
	registerResp       *usecase.AuthResponse
	loginResp          *usecase.AuthResponse
	refreshTokenResp   *usecase.AuthResponse
	registerCalled     bool
	loginCalled        bool
	refreshTokenCalled bool
	logoutCalled       bool
}

func newMockAuthUseCase() *mockAuthUseCase {
	return &mockAuthUseCase{
		registerResp: &usecase.AuthResponse{
			AccessToken:  "access_token",
			RefreshToken: "refresh_token",
			User: &usecase.UserResponse{
				ID:       1,
				Username: "testuser",
				Role:     domain.RoleAdmin,
			},
		},
		loginResp: &usecase.AuthResponse{
			AccessToken:  "access_token",
			RefreshToken: "refresh_token",
			User: &usecase.UserResponse{
				ID:       1,
				Username: "testuser",
				Role:     domain.RoleAdmin,
			},
		},
		refreshTokenResp: &usecase.AuthResponse{
			AccessToken:  "new_access_token",
			RefreshToken: "new_refresh_token",
			User: &usecase.UserResponse{
				ID:       1,
				Username: "testuser",
				Role:     domain.RoleAdmin,
			},
		},
	}
}

func (m *mockAuthUseCase) Register(ctx context.Context, req *usecase.RegisterRequest) (*usecase.AuthResponse, error) {
	m.registerCalled = true
	if m.registerErr != nil {
		return nil, m.registerErr
	}
	return m.registerResp, nil
}

func (m *mockAuthUseCase) Login(ctx context.Context, req *usecase.LoginRequest) (*usecase.AuthResponse, error) {
	m.loginCalled = true
	if m.loginErr != nil {
		return nil, m.loginErr
	}
	return m.loginResp, nil
}

func (m *mockAuthUseCase) RefreshToken(ctx context.Context, refreshToken string) (*usecase.AuthResponse, error) {
	m.refreshTokenCalled = true
	if m.refreshTokenErr != nil {
		return nil, m.refreshTokenErr
	}
	return m.refreshTokenResp, nil
}

func (m *mockAuthUseCase) Logout(ctx context.Context, refreshToken string) error {
	m.logoutCalled = true
	if m.logoutErr != nil {
		return m.logoutErr
	}
	return nil
}

func TestAuthHandler_Register(t *testing.T) {
	tests := []struct {
		name           string
		body           interface{}
		setup          func(*mockAuthUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockAuthUseCase)
	}{
		{
			name: "successful registration",
			body: RegisterRequest{
				Username: "testuser",
				Email:    stringPtr("test@example.com"),
				Password: "password123",
				Role:     "admin",
			},
			setup:          func(m *mockAuthUseCase) {},
			wantStatusCode: http.StatusCreated,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockAuthUseCase) {
				if !m.registerCalled {
					t.Error("expected Register to be called")
				}
				var resp AuthResponse
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if resp.AccessToken == "" {
					t.Error("expected access token")
				}
				if resp.User == nil {
					t.Fatal("expected user")
				}
			},
		},
		{
			name: "missing username",
			body: RegisterRequest{
				Password: "password123",
				Role:     "admin",
			},
			setup:          func(m *mockAuthUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
		{
			name: "missing password",
			body: RegisterRequest{
				Username: "testuser",
				Role:     "admin",
			},
			setup:          func(m *mockAuthUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
		{
			name: "invalid role",
			body: RegisterRequest{
				Username: "testuser",
				Password: "password123",
				Role:     "invalid",
			},
			setup:          func(m *mockAuthUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
		{
			name:           "invalid JSON",
			body:           "invalid json",
			setup:          func(m *mockAuthUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
		{
			name: "usecase error",
			body: RegisterRequest{
				Username: "testuser",
				Password: "password123",
				Role:     "admin",
			},
			setup: func(m *mockAuthUseCase) {
				m.registerErr = domain.NewAlreadyExistsError("User", "username", "testuser", "user already exists")
			},
			wantStatusCode: http.StatusConflict,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockAuthUseCase()
			tt.setup(mockUC)

			handler := NewAuthHandler(mockUC, &mockLogger{})

			var body []byte
			var err error
			if tt.body != nil {
				body, err = json.Marshal(tt.body)
				if err != nil {
					t.Fatalf("failed to marshal body: %v", err)
				}
			}

			req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/register", bytes.NewReader(body))
			req.Header.Set("Content-Type", "application/json")
			w := httptest.NewRecorder()

			handler.Register(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}

func TestAuthHandler_Login(t *testing.T) {
	tests := []struct {
		name           string
		body           interface{}
		setup          func(*mockAuthUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockAuthUseCase)
	}{
		{
			name: "successful login",
			body: LoginRequest{
				Username: "testuser",
				Password: "password123",
			},
			setup:          func(m *mockAuthUseCase) {},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockAuthUseCase) {
				if !m.loginCalled {
					t.Error("expected Login to be called")
				}
				var resp AuthResponse
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if resp.AccessToken == "" {
					t.Error("expected access token")
				}
			},
		},
		{
			name: "missing username",
			body: LoginRequest{
				Password: "password123",
			},
			setup:          func(m *mockAuthUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
		{
			name: "missing password",
			body: LoginRequest{
				Username: "testuser",
			},
			setup:          func(m *mockAuthUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
		{
			name: "invalid credentials",
			body: LoginRequest{
				Username: "testuser",
				Password: "wrongpassword",
			},
			setup: func(m *mockAuthUseCase) {
				m.loginErr = domain.NewValidationError("User", "password", "", "invalid username or password")
			},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockAuthUseCase()
			tt.setup(mockUC)

			handler := NewAuthHandler(mockUC, &mockLogger{})

			body, err := json.Marshal(tt.body)
			if err != nil {
				t.Fatalf("failed to marshal body: %v", err)
			}

			req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", bytes.NewReader(body))
			req.Header.Set("Content-Type", "application/json")
			w := httptest.NewRecorder()

			handler.Login(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}

func TestAuthHandler_RefreshToken(t *testing.T) {
	tests := []struct {
		name           string
		body           interface{}
		setup          func(*mockAuthUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockAuthUseCase)
	}{
		{
			name: "successful refresh",
			body: RefreshTokenRequest{
				RefreshToken: "valid_refresh_token",
			},
			setup:          func(m *mockAuthUseCase) {},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockAuthUseCase) {
				if !m.refreshTokenCalled {
					t.Error("expected RefreshToken to be called")
				}
				var resp AuthResponse
				if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
					t.Fatalf("failed to unmarshal response: %v", err)
				}
				if resp.AccessToken == "" {
					t.Error("expected access token")
				}
			},
		},
		{
			name:           "missing refresh token",
			body:           RefreshTokenRequest{},
			setup:          func(m *mockAuthUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
		{
			name: "invalid token",
			body: RefreshTokenRequest{
				RefreshToken: "invalid_token",
			},
			setup: func(m *mockAuthUseCase) {
				m.refreshTokenErr = domain.NewValidationError("JWT", "", "", "invalid refresh token")
			},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockAuthUseCase()
			tt.setup(mockUC)

			handler := NewAuthHandler(mockUC, &mockLogger{})

			body, err := json.Marshal(tt.body)
			if err != nil {
				t.Fatalf("failed to marshal body: %v", err)
			}

			req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/refresh", bytes.NewReader(body))
			req.Header.Set("Content-Type", "application/json")
			w := httptest.NewRecorder()

			handler.RefreshToken(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}

func TestAuthHandler_Logout(t *testing.T) {
	tests := []struct {
		name           string
		body           interface{}
		setup          func(*mockAuthUseCase)
		wantStatusCode int
		wantErr        bool
		check          func(*testing.T, *httptest.ResponseRecorder, *mockAuthUseCase)
	}{
		{
			name: "successful logout",
			body: RefreshTokenRequest{
				RefreshToken: "valid_refresh_token",
			},
			setup:          func(m *mockAuthUseCase) {},
			wantStatusCode: http.StatusOK,
			wantErr:        false,
			check: func(t *testing.T, w *httptest.ResponseRecorder, m *mockAuthUseCase) {
				if !m.logoutCalled {
					t.Error("expected Logout to be called")
				}
			},
		},
		{
			name:           "missing refresh token",
			body:           RefreshTokenRequest{},
			setup:          func(m *mockAuthUseCase) {},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
		{
			name: "invalid token",
			body: RefreshTokenRequest{
				RefreshToken: "invalid_token",
			},
			setup: func(m *mockAuthUseCase) {
				m.logoutErr = domain.NewValidationError("JWT", "", "", "invalid refresh token")
			},
			wantStatusCode: http.StatusBadRequest,
			wantErr:        true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockUC := newMockAuthUseCase()
			tt.setup(mockUC)

			handler := NewAuthHandler(mockUC, &mockLogger{})

			body, err := json.Marshal(tt.body)
			if err != nil {
				t.Fatalf("failed to marshal body: %v", err)
			}

			req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/logout", bytes.NewReader(body))
			req.Header.Set("Content-Type", "application/json")
			w := httptest.NewRecorder()

			handler.Logout(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil {
				tt.check(t, w, mockUC)
			}
		})
	}
}

type mockLogger struct{}

func (m *mockLogger) Debug(msg string, args ...any) {}
func (m *mockLogger) Info(msg string, args ...any)  {}
func (m *mockLogger) Warn(msg string, args ...any)  {}
func (m *mockLogger) Error(msg string, args ...any) {}
func (m *mockLogger) WithContext(ctx context.Context) logger.Logger {
	return m
}
func (m *mockLogger) WithRequestID(requestID string) logger.Logger {
	return m
}
func (m *mockLogger) WithError(err error) logger.Logger {
	return m
}

func stringPtr(s string) *string {
	return &s
}
