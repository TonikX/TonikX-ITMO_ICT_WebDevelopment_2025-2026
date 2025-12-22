package middleware

import (
	"context"
	"net/http"
	"net/http/httptest"
	"testing"

	"school-service/internal/ctx"
	"school-service/internal/domain"
)

type mockJWTService struct {
	validateAccessTokenErr error
	claims                 *domain.TokenClaims
	validateCalled         bool
}

func newMockJWTService() *mockJWTService {
	return &mockJWTService{
		claims: &domain.TokenClaims{
			UserID:   1,
			Username: "testuser",
			Role:     domain.RoleAdmin,
		},
	}
}

func (m *mockJWTService) GenerateAccessToken(userID int, username string, role domain.UserRole) (string, error) {
	return "access_token", nil
}

func (m *mockJWTService) GenerateRefreshToken(userID int) (string, string, error) {
	return "refresh_token", "token_hash", nil
}

func (m *mockJWTService) HashRefreshToken(token string) string {
	return "token_hash"
}

func (m *mockJWTService) ValidateAccessToken(tokenString string) (*domain.TokenClaims, error) {
	m.validateCalled = true
	if m.validateAccessTokenErr != nil {
		return nil, m.validateAccessTokenErr
	}
	return m.claims, nil
}

func (m *mockJWTService) ValidateRefreshToken(tokenString string) (*domain.TokenClaims, error) {
	return m.claims, nil
}

func TestAuthMiddleware(t *testing.T) {
	tests := []struct {
		name           string
		authHeader     string
		setup          func(*mockJWTService)
		wantStatusCode int
		wantCalled     bool
		check          func(*testing.T, *httptest.ResponseRecorder, *http.Request, *mockJWTService)
	}{
		{
			name:           "successful authentication",
			authHeader:     "Bearer valid_token",
			setup:          func(m *mockJWTService) {},
			wantStatusCode: http.StatusOK,
			wantCalled:     true,
			check: func(t *testing.T, w *httptest.ResponseRecorder, r *http.Request, m *mockJWTService) {
				if !m.validateCalled {
					t.Error("expected ValidateAccessToken to be called")
				}
			},
		},
		{
			name:           "missing authorization header",
			authHeader:     "",
			setup:          func(m *mockJWTService) {},
			wantStatusCode: http.StatusUnauthorized,
			wantCalled:     false,
		},
		{
			name:           "invalid authorization header format",
			authHeader:     "InvalidFormat token",
			setup:          func(m *mockJWTService) {},
			wantStatusCode: http.StatusUnauthorized,
			wantCalled:     false,
		},
		{
			name:       "invalid token",
			authHeader: "Bearer invalid_token",
			setup: func(m *mockJWTService) {
				m.validateAccessTokenErr = domain.NewValidationError("JWT", "", "", "invalid token")
			},
			wantStatusCode: http.StatusUnauthorized,
			wantCalled:     true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockJWT := newMockJWTService()
			tt.setup(mockJWT)

			handler := AuthMiddleware(mockJWT)
			var capturedReq *http.Request
			nextHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				capturedReq = r
				w.WriteHeader(http.StatusOK)
			})

			req := httptest.NewRequest(http.MethodGet, "/test", nil)
			if tt.authHeader != "" {
				req.Header.Set("Authorization", tt.authHeader)
			}
			w := httptest.NewRecorder()

			handler(nextHandler).ServeHTTP(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if tt.check != nil && capturedReq != nil {
				if tt.name == "successful authentication" {
					userID, ok := capturedReq.Context().Value(ctx.UserIDKey).(int)
					if !ok || userID != 1 {
						t.Errorf("expected userID 1 in context, got %v", userID)
					}
					username, ok := capturedReq.Context().Value(ctx.UsernameKey).(string)
					if !ok || username != "testuser" {
						t.Errorf("expected username testuser in context, got %v", username)
					}
					role, ok := capturedReq.Context().Value(ctx.UserRoleKey).(domain.UserRole)
					if !ok || role != domain.RoleAdmin {
						t.Errorf("expected role admin in context, got %v", role)
					}
				}
				tt.check(t, w, capturedReq, mockJWT)
			}
		})
	}
}

func TestRequireRole(t *testing.T) {
	tests := []struct {
		name           string
		roleInContext  domain.UserRole
		allowedRoles   []domain.UserRole
		wantStatusCode int
		wantCalled     bool
	}{
		{
			name:           "admin access with admin role",
			roleInContext:  domain.RoleAdmin,
			allowedRoles:   []domain.UserRole{domain.RoleAdmin, domain.RoleHeadTeacher},
			wantStatusCode: http.StatusOK,
			wantCalled:     true,
		},
		{
			name:           "head_teacher access with head_teacher role",
			roleInContext:  domain.RoleHeadTeacher,
			allowedRoles:   []domain.UserRole{domain.RoleAdmin, domain.RoleHeadTeacher},
			wantStatusCode: http.StatusOK,
			wantCalled:     true,
		},
		{
			name:           "teacher denied access",
			roleInContext:  domain.RoleTeacher,
			allowedRoles:   []domain.UserRole{domain.RoleAdmin, domain.RoleHeadTeacher},
			wantStatusCode: http.StatusForbidden,
			wantCalled:     false,
		},
		{
			name:           "no role in context",
			roleInContext:  "",
			allowedRoles:   []domain.UserRole{domain.RoleAdmin},
			wantStatusCode: http.StatusUnauthorized,
			wantCalled:     false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			handler := RequireRole(tt.allowedRoles...)
			nextHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				w.WriteHeader(http.StatusOK)
			})

			req := httptest.NewRequest(http.MethodGet, "/test", nil)
			if tt.roleInContext != "" {
				req = req.WithContext(context.WithValue(req.Context(), ctx.UserRoleKey, tt.roleInContext))
			}
			w := httptest.NewRecorder()

			called := false
			wrappedNext := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				called = true
				nextHandler.ServeHTTP(w, r)
			})

			handler(wrappedNext).ServeHTTP(w, req)

			if w.Code != tt.wantStatusCode {
				t.Errorf("expected status code %d, got %d", tt.wantStatusCode, w.Code)
			}

			if called != tt.wantCalled {
				t.Errorf("expected called=%v, got %v", tt.wantCalled, called)
			}
		})
	}
}
