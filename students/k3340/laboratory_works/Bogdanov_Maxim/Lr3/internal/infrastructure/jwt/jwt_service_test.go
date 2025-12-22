package jwt

import (
	"testing"
	"time"

	"school-service/internal/domain"
	mockclock "school-service/internal/infrastructure/clock"
	realclock "school-service/internal/infrastructure/clock"
)

func TestJWTService_GenerateAccessToken(t *testing.T) {
	clock := realclock.NewRealClock()
	service := NewJWTService(JWTConfig{
		AccessSecret:  "test_secret",
		RefreshSecret: "test_refresh_secret",
		AccessTTL:     15 * time.Minute,
		RefreshTTL:    7 * 24 * time.Hour,
		Clock:         clock,
	})

	token, err := service.GenerateAccessToken(1, "testuser", domain.RoleAdmin)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if token == "" {
		t.Error("expected non-empty token")
	}

	claims, err := service.ValidateAccessToken(token)
	if err != nil {
		t.Fatalf("failed to validate generated token: %v", err)
	}

	if claims.UserID != 1 {
		t.Errorf("expected UserID 1, got %d", claims.UserID)
	}
	if claims.Username != "testuser" {
		t.Errorf("expected Username testuser, got %s", claims.Username)
	}
	if claims.Role != domain.RoleAdmin {
		t.Errorf("expected Role admin, got %s", claims.Role)
	}
}

func TestJWTService_GenerateRefreshToken(t *testing.T) {
	clock := realclock.NewRealClock()
	service := NewJWTService(JWTConfig{
		AccessSecret:  "test_secret",
		RefreshSecret: "test_refresh_secret",
		AccessTTL:     15 * time.Minute,
		RefreshTTL:    7 * 24 * time.Hour,
		Clock:         clock,
	})

	token, hash, err := service.GenerateRefreshToken(1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if token == "" {
		t.Error("expected non-empty token")
	}
	if hash == "" {
		t.Error("expected non-empty hash")
	}

	claims, err := service.ValidateRefreshToken(token)
	if err != nil {
		t.Fatalf("failed to validate generated token: %v", err)
	}

	if claims.UserID != 1 {
		t.Errorf("expected UserID 1, got %d", claims.UserID)
	}

	calculatedHash := service.HashRefreshToken(token)
	if calculatedHash != hash {
		t.Errorf("expected hash %s, got %s", hash, calculatedHash)
	}
}

func TestJWTService_ValidateAccessToken(t *testing.T) {
	clock := realclock.NewRealClock()
	service := NewJWTService(JWTConfig{
		AccessSecret:  "test_secret",
		RefreshSecret: "test_refresh_secret",
		AccessTTL:     15 * time.Minute,
		RefreshTTL:    7 * 24 * time.Hour,
		Clock:         clock,
	})

	tests := []struct {
		name    string
		setup   func() (string, domain.JWTService)
		wantErr bool
		check   func(*testing.T, *domain.TokenClaims)
	}{
		{
			name: "valid token",
			setup: func() (string, domain.JWTService) {
				testClock := realclock.NewRealClock()
				testService := NewJWTService(JWTConfig{
					AccessSecret:  "test_secret",
					RefreshSecret: "test_refresh_secret",
					AccessTTL:     15 * time.Minute,
					RefreshTTL:    7 * 24 * time.Hour,
					Clock:         testClock,
				})
				token, _ := testService.GenerateAccessToken(1, "testuser", domain.RoleAdmin)
				return token, testService
			},
			wantErr: false,
			check: func(t *testing.T, claims *domain.TokenClaims) {
				if claims.UserID != 1 {
					t.Errorf("expected UserID 1, got %d", claims.UserID)
				}
				if claims.Username != "testuser" {
					t.Errorf("expected Username testuser, got %s", claims.Username)
				}
			},
		},
		{
			name: "invalid token",
			setup: func() (string, domain.JWTService) {
				return "invalid.token.here", service
			},
			wantErr: true,
		},
		{
			name: "expired token",
			setup: func() (string, domain.JWTService) {
				expiredClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
				expiredService := NewJWTService(JWTConfig{
					AccessSecret:  "test_secret",
					RefreshSecret: "test_refresh_secret",
					AccessTTL:     1 * time.Minute,
					RefreshTTL:    7 * 24 * time.Hour,
					Clock:         expiredClock,
				})
				token, _ := expiredService.GenerateAccessToken(1, "testuser", domain.RoleAdmin)
				expiredClock.Advance(2 * time.Minute)
				return token, expiredService
			},
			wantErr: true,
		},
		{
			name: "wrong secret",
			setup: func() (string, domain.JWTService) {
				wrongService := NewJWTService(JWTConfig{
					AccessSecret:  "wrong_secret",
					RefreshSecret: "test_refresh_secret",
					AccessTTL:     15 * time.Minute,
					RefreshTTL:    7 * 24 * time.Hour,
					Clock:         clock,
				})
				token, _ := wrongService.GenerateAccessToken(1, "testuser", domain.RoleAdmin)
				return token, service
			},
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			token, testService := tt.setup()
			claims, err := testService.ValidateAccessToken(token)

			if tt.wantErr {
				if err == nil {
					t.Error("expected error, got nil")
				}
				return
			}

			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}

			if tt.check != nil {
				tt.check(t, claims)
			}
		})
	}
}

func TestJWTService_ValidateRefreshToken(t *testing.T) {
	clock := realclock.NewRealClock()
	service := NewJWTService(JWTConfig{
		AccessSecret:  "test_secret",
		RefreshSecret: "test_refresh_secret",
		AccessTTL:     15 * time.Minute,
		RefreshTTL:    7 * 24 * time.Hour,
		Clock:         clock,
	})

	tests := []struct {
		name    string
		setup   func() (string, domain.JWTService)
		wantErr bool
		check   func(*testing.T, *domain.TokenClaims)
	}{
		{
			name: "valid token",
			setup: func() (string, domain.JWTService) {
				realClock := realclock.NewRealClock()
				testService := NewJWTService(JWTConfig{
					AccessSecret:  "test_secret",
					RefreshSecret: "test_refresh_secret",
					AccessTTL:     15 * time.Minute,
					RefreshTTL:    7 * 24 * time.Hour,
					Clock:         realClock,
				})
				token, _, _ := testService.GenerateRefreshToken(1)
				return token, testService
			},
			wantErr: false,
			check: func(t *testing.T, claims *domain.TokenClaims) {
				if claims.UserID != 1 {
					t.Errorf("expected UserID 1, got %d", claims.UserID)
				}
			},
		},
		{
			name: "invalid token",
			setup: func() (string, domain.JWTService) {
				return "invalid.token.here", service
			},
			wantErr: true,
		},
		{
			name: "expired token",
			setup: func() (string, domain.JWTService) {
				expiredClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
				expiredService := NewJWTService(JWTConfig{
					AccessSecret:  "test_secret",
					RefreshSecret: "test_refresh_secret",
					AccessTTL:     15 * time.Minute,
					RefreshTTL:    1 * time.Hour,
					Clock:         expiredClock,
				})
				token, _, _ := expiredService.GenerateRefreshToken(1)
				expiredClock.Advance(2 * time.Hour)
				return token, expiredService
			},
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			token, testService := tt.setup()
			claims, err := testService.ValidateRefreshToken(token)

			if tt.wantErr {
				if err == nil {
					t.Error("expected error, got nil")
				}
				return
			}

			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}

			if tt.check != nil {
				tt.check(t, claims)
			}
		})
	}
}

func TestJWTService_HashRefreshToken(t *testing.T) {
	clock := realclock.NewRealClock()
	service := NewJWTService(JWTConfig{
		AccessSecret:  "test_secret",
		RefreshSecret: "test_refresh_secret",
		AccessTTL:     15 * time.Minute,
		RefreshTTL:    7 * 24 * time.Hour,
		Clock:         clock,
	})

	token := "test_token_123"
	hash1 := service.HashRefreshToken(token)
	hash2 := service.HashRefreshToken(token)

	if hash1 != hash2 {
		t.Error("expected same hash for same token")
	}

	if hash1 == "" {
		t.Error("expected non-empty hash")
	}

	differentHash := service.HashRefreshToken("different_token")
	if hash1 == differentHash {
		t.Error("expected different hash for different token")
	}
}
