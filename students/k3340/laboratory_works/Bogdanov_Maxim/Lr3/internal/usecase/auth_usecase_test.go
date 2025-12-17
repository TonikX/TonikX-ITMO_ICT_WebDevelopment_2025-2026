package usecase

import (
	"context"
	"errors"
	"testing"
	"time"

	"school-service/internal/domain"
	"school-service/internal/domain/clock"
	"school-service/internal/domain/usecase"
	mockclock "school-service/internal/infrastructure/clock"
)

type mockUserRepository struct {
	users            map[int]*domain.User
	usersByUsername  map[string]*domain.User
	usersByEmail     map[string]*domain.User
	createErr        error
	getByIDErr       error
	getByUsernameErr error
	getByEmailErr    error
	updateErr        error
	deleteErr        error
	createCalled     bool
	updateCalled     bool
	deleteCalled     bool
}

func newMockUserRepository() *mockUserRepository {
	return &mockUserRepository{
		users:           make(map[int]*domain.User),
		usersByUsername: make(map[string]*domain.User),
		usersByEmail:    make(map[string]*domain.User),
	}
}

func (m *mockUserRepository) Create(ctx context.Context, user *domain.User) error {
	m.createCalled = true
	if m.createErr != nil {
		return m.createErr
	}
	user.SetID(len(m.users) + 1)
	m.users[user.ID] = user
	m.usersByUsername[user.Username] = user
	if user.Email != nil {
		m.usersByEmail[*user.Email] = user
	}
	return nil
}

func (m *mockUserRepository) GetByID(ctx context.Context, id int) (*domain.User, error) {
	if m.getByIDErr != nil {
		return nil, m.getByIDErr
	}
	user, ok := m.users[id]
	if !ok {
		return nil, domain.NewNotFoundError("User", "id", id, "user not found")
	}
	return user, nil
}

func (m *mockUserRepository) GetByUsername(ctx context.Context, username string) (*domain.User, error) {
	if m.getByUsernameErr != nil {
		return nil, m.getByUsernameErr
	}
	user, ok := m.usersByUsername[username]
	if !ok {
		return nil, domain.NewNotFoundError("User", "username", username, "user not found")
	}
	return user, nil
}

func (m *mockUserRepository) GetByEmail(ctx context.Context, email string) (*domain.User, error) {
	if m.getByEmailErr != nil {
		return nil, m.getByEmailErr
	}
	user, ok := m.usersByEmail[email]
	if !ok {
		return nil, domain.NewNotFoundError("User", "email", email, "user not found")
	}
	return user, nil
}

func (m *mockUserRepository) Update(ctx context.Context, user *domain.User) error {
	m.updateCalled = true
	if m.updateErr != nil {
		return m.updateErr
	}
	if _, ok := m.users[user.ID]; !ok {
		return domain.NewNotFoundError("User", "id", user.ID, "user not found")
	}
	m.users[user.ID] = user
	m.usersByUsername[user.Username] = user
	if user.Email != nil {
		m.usersByEmail[*user.Email] = user
	}
	return nil
}

func (m *mockUserRepository) Delete(ctx context.Context, id int) error {
	m.deleteCalled = true
	if m.deleteErr != nil {
		return m.deleteErr
	}
	if _, ok := m.users[id]; !ok {
		return domain.NewNotFoundError("User", "id", id, "user not found")
	}
	delete(m.users, id)
	return nil
}

type mockRefreshTokenRepository struct {
	tokens            map[string]*domain.RefreshToken
	tokensByUser      map[int][]*domain.RefreshToken
	createErr         error
	getByTokenHashErr error
	getByUserIDErr    error
	revokeErr         error
	revokeAllErr      error
	deleteExpiredErr  error
	createCalled      bool
	revokeCalled      bool
}

func newMockRefreshTokenRepository() *mockRefreshTokenRepository {
	return &mockRefreshTokenRepository{
		tokens:       make(map[string]*domain.RefreshToken),
		tokensByUser: make(map[int][]*domain.RefreshToken),
	}
}

func (m *mockRefreshTokenRepository) Create(ctx context.Context, token *domain.RefreshToken) error {
	m.createCalled = true
	if m.createErr != nil {
		return m.createErr
	}
	token.SetID(len(m.tokens) + 1)
	m.tokens[token.TokenHash] = token
	m.tokensByUser[token.UserID] = append(m.tokensByUser[token.UserID], token)
	return nil
}

func (m *mockRefreshTokenRepository) GetByTokenHash(ctx context.Context, tokenHash string) (*domain.RefreshToken, error) {
	if m.getByTokenHashErr != nil {
		return nil, m.getByTokenHashErr
	}
	token, ok := m.tokens[tokenHash]
	if !ok {
		return nil, domain.NewNotFoundError("RefreshToken", "token_hash", tokenHash, "refresh token not found")
	}
	return token, nil
}

func (m *mockRefreshTokenRepository) GetByUserID(ctx context.Context, userID int) ([]*domain.RefreshToken, error) {
	if m.getByUserIDErr != nil {
		return nil, m.getByUserIDErr
	}
	return m.tokensByUser[userID], nil
}

func (m *mockRefreshTokenRepository) Revoke(ctx context.Context, tokenHash string) error {
	m.revokeCalled = true
	if m.revokeErr != nil {
		return m.revokeErr
	}
	token, ok := m.tokens[tokenHash]
	if !ok {
		return domain.NewNotFoundError("RefreshToken", "token_hash", tokenHash, "refresh token not found")
	}
	now := time.Now()
	token.RevokedAt = &now
	return nil
}

func (m *mockRefreshTokenRepository) RevokeAllForUser(ctx context.Context, userID int) error {
	if m.revokeAllErr != nil {
		return m.revokeAllErr
	}
	now := time.Now()
	for _, token := range m.tokensByUser[userID] {
		token.RevokedAt = &now
	}
	return nil
}

func (m *mockRefreshTokenRepository) DeleteExpired(ctx context.Context, before time.Time) error {
	if m.deleteExpiredErr != nil {
		return m.deleteExpiredErr
	}
	for hash, token := range m.tokens {
		if token.ExpiresAt.Before(before) {
			delete(m.tokens, hash)
		}
	}
	return nil
}

type mockPasswordHasher struct {
	hashErr      error
	verifyErr    error
	hashCalled   bool
	verifyCalled bool
}

func newMockPasswordHasher() *mockPasswordHasher {
	return &mockPasswordHasher{}
}

func (m *mockPasswordHasher) Hash(password string) (string, error) {
	m.hashCalled = true
	if m.hashErr != nil {
		return "", m.hashErr
	}
	return "hashed_" + password, nil
}

func (m *mockPasswordHasher) Verify(hashedPassword, password string) error {
	m.verifyCalled = true
	if m.verifyErr != nil {
		return m.verifyErr
	}
	if hashedPassword != "hashed_"+password {
		return domain.NewValidationError("Password", "", "", "invalid password")
	}
	return nil
}

type mockJWTService struct {
	generateAccessTokenErr  error
	generateRefreshTokenErr error
	validateAccessTokenErr  error
	validateRefreshTokenErr error
	hashRefreshTokenErr     error
	accessToken             string
	refreshToken            string
	tokenHash               string
	claims                  *domain.TokenClaims
	generateAccessCalled    bool
	generateRefreshCalled   bool
	validateAccessCalled    bool
	validateRefreshCalled   bool
}

func newMockJWTService() *mockJWTService {
	return &mockJWTService{
		accessToken:  "access_token_123",
		refreshToken: "refresh_token_123",
		tokenHash:    "token_hash_123",
		claims: &domain.TokenClaims{
			UserID:    1,
			Username:  "testuser",
			Role:      domain.RoleAdmin,
			ExpiresAt: time.Now().Add(time.Hour),
		},
	}
}

func (m *mockJWTService) GenerateAccessToken(userID int, username string, role domain.UserRole) (string, error) {
	m.generateAccessCalled = true
	if m.generateAccessTokenErr != nil {
		return "", m.generateAccessTokenErr
	}
	return m.accessToken, nil
}

func (m *mockJWTService) GenerateRefreshToken(userID int) (string, string, error) {
	m.generateRefreshCalled = true
	if m.generateRefreshTokenErr != nil {
		return "", "", m.generateRefreshTokenErr
	}
	return m.refreshToken, m.tokenHash, nil
}

func (m *mockJWTService) HashRefreshToken(token string) string {
	return m.tokenHash
}

func (m *mockJWTService) ValidateAccessToken(tokenString string) (*domain.TokenClaims, error) {
	m.validateAccessCalled = true
	if m.validateAccessTokenErr != nil {
		return nil, m.validateAccessTokenErr
	}
	return m.claims, nil
}

func (m *mockJWTService) ValidateRefreshToken(tokenString string) (*domain.TokenClaims, error) {
	m.validateRefreshCalled = true
	if m.validateRefreshTokenErr != nil {
		return nil, m.validateRefreshTokenErr
	}
	return m.claims, nil
}

func TestAuthUseCase_Register(t *testing.T) {
	tests := []struct {
		name    string
		req     *usecase.RegisterRequest
		setup   func(*mockUserRepository, *mockRefreshTokenRepository, *mockPasswordHasher, *mockJWTService)
		wantErr bool
		check   func(*testing.T, *usecase.AuthResponse, *mockUserRepository, *mockRefreshTokenRepository, *mockPasswordHasher, *mockJWTService)
	}{
		{
			name: "successful registration",
			req: &usecase.RegisterRequest{
				Username: "testuser",
				Email:    stringPtr("test@example.com"),
				Password: "password123",
				Role:     domain.RoleAdmin,
			},
			setup: func(userRepo *mockUserRepository, tokenRepo *mockRefreshTokenRepository, hasher *mockPasswordHasher, jwt *mockJWTService) {
			},
			wantErr: false,
			check: func(t *testing.T, resp *usecase.AuthResponse, userRepo *mockUserRepository, tokenRepo *mockRefreshTokenRepository, hasher *mockPasswordHasher, jwt *mockJWTService) {
				if resp == nil {
					t.Fatal("expected response, got nil")
				}
				if resp.AccessToken == "" {
					t.Error("expected access token")
				}
				if resp.RefreshToken == "" {
					t.Error("expected refresh token")
				}
				if resp.User == nil {
					t.Fatal("expected user, got nil")
				}
				if resp.User.Username != "testuser" {
					t.Errorf("expected username testuser, got %s", resp.User.Username)
				}
				if !userRepo.createCalled {
					t.Error("expected Create to be called")
				}
				if !hasher.hashCalled {
					t.Error("expected Hash to be called")
				}
				if !jwt.generateAccessCalled {
					t.Error("expected GenerateAccessToken to be called")
				}
				if !jwt.generateRefreshCalled {
					t.Error("expected GenerateRefreshToken to be called")
				}
				if !tokenRepo.createCalled {
					t.Error("expected Create to be called on token repo")
				}
			},
		},
		{
			name: "username already exists",
			req: &usecase.RegisterRequest{
				Username: "existing",
				Password: "password123",
				Role:     domain.RoleAdmin,
			},
			setup: func(userRepo *mockUserRepository, tokenRepo *mockRefreshTokenRepository, hasher *mockPasswordHasher, jwt *mockJWTService) {
				userRepo.usersByUsername["existing"] = &domain.User{ID: 1, Username: "existing"}
			},
			wantErr: true,
		},
		{
			name: "email already exists",
			req: &usecase.RegisterRequest{
				Username: "newuser",
				Email:    stringPtr("existing@example.com"),
				Password: "password123",
				Role:     domain.RoleAdmin,
			},
			setup: func(userRepo *mockUserRepository, tokenRepo *mockRefreshTokenRepository, hasher *mockPasswordHasher, jwt *mockJWTService) {
				userRepo.usersByEmail["existing@example.com"] = &domain.User{ID: 1, Email: stringPtr("existing@example.com")}
			},
			wantErr: true,
		},
		{
			name: "invalid role",
			req: &usecase.RegisterRequest{
				Username: "testuser",
				Password: "password123",
				Role:     domain.UserRole("invalid"),
			},
			setup: func(userRepo *mockUserRepository, tokenRepo *mockRefreshTokenRepository, hasher *mockPasswordHasher, jwt *mockJWTService) {
			},
			wantErr: true,
		},
		{
			name: "password hash error",
			req: &usecase.RegisterRequest{
				Username: "testuser",
				Password: "password123",
				Role:     domain.RoleAdmin,
			},
			setup: func(userRepo *mockUserRepository, tokenRepo *mockRefreshTokenRepository, hasher *mockPasswordHasher, jwt *mockJWTService) {
				hasher.hashErr = errors.New("hash error")
			},
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			userRepo := newMockUserRepository()
			tokenRepo := newMockRefreshTokenRepository()
			hasher := newMockPasswordHasher()
			jwt := newMockJWTService()
			clock := mockclock.NewMockClock(time.Now())
			logger := &mockLogger{}
			refreshTTL := 7 * 24 * time.Hour

			tt.setup(userRepo, tokenRepo, hasher, jwt)

			uc := NewAuthUseCase(userRepo, tokenRepo, hasher, jwt, clock, logger, refreshTTL)

			resp, err := uc.Register(context.Background(), tt.req)

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
				tt.check(t, resp, userRepo, tokenRepo, hasher, jwt)
			}
		})
	}
}

func TestAuthUseCase_Login(t *testing.T) {
	tests := []struct {
		name    string
		req     *usecase.LoginRequest
		setup   func(*mockUserRepository, *mockRefreshTokenRepository, *mockPasswordHasher, *mockJWTService)
		wantErr bool
		check   func(*testing.T, *usecase.AuthResponse, *mockUserRepository, *mockRefreshTokenRepository, *mockPasswordHasher, *mockJWTService)
	}{
		{
			name: "successful login",
			req: &usecase.LoginRequest{
				Username: "testuser",
				Password: "password123",
			},
			setup: func(userRepo *mockUserRepository, tokenRepo *mockRefreshTokenRepository, hasher *mockPasswordHasher, jwt *mockJWTService) {
				userRepo.usersByUsername["testuser"] = &domain.User{
					ID:           1,
					Username:     "testuser",
					PasswordHash: "hashed_password123",
					Role:         domain.RoleAdmin,
					IsActive:     true,
				}
			},
			wantErr: false,
			check: func(t *testing.T, resp *usecase.AuthResponse, userRepo *mockUserRepository, tokenRepo *mockRefreshTokenRepository, hasher *mockPasswordHasher, jwt *mockJWTService) {
				if resp == nil {
					t.Fatal("expected response, got nil")
				}
				if !hasher.verifyCalled {
					t.Error("expected Verify to be called")
				}
				if !jwt.generateAccessCalled {
					t.Error("expected GenerateAccessToken to be called")
				}
				if !jwt.generateRefreshCalled {
					t.Error("expected GenerateRefreshToken to be called")
				}
				if !tokenRepo.createCalled {
					t.Error("expected Create to be called on token repo")
				}
			},
		},
		{
			name: "user not found",
			req: &usecase.LoginRequest{
				Username: "nonexistent",
				Password: "password123",
			},
			setup: func(userRepo *mockUserRepository, tokenRepo *mockRefreshTokenRepository, hasher *mockPasswordHasher, jwt *mockJWTService) {
			},
			wantErr: true,
		},
		{
			name: "invalid password",
			req: &usecase.LoginRequest{
				Username: "testuser",
				Password: "wrongpassword",
			},
			setup: func(userRepo *mockUserRepository, tokenRepo *mockRefreshTokenRepository, hasher *mockPasswordHasher, jwt *mockJWTService) {
				userRepo.usersByUsername["testuser"] = &domain.User{
					ID:           1,
					Username:     "testuser",
					PasswordHash: "hashed_password123",
					Role:         domain.RoleAdmin,
					IsActive:     true,
				}
				hasher.verifyErr = domain.NewValidationError("Password", "", "", "invalid password")
			},
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			userRepo := newMockUserRepository()
			tokenRepo := newMockRefreshTokenRepository()
			hasher := newMockPasswordHasher()
			jwt := newMockJWTService()
			clock := mockclock.NewMockClock(time.Now())
			logger := &mockLogger{}
			refreshTTL := 7 * 24 * time.Hour

			tt.setup(userRepo, tokenRepo, hasher, jwt)

			uc := NewAuthUseCase(userRepo, tokenRepo, hasher, jwt, clock, logger, refreshTTL)

			resp, err := uc.Login(context.Background(), tt.req)

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
				tt.check(t, resp, userRepo, tokenRepo, hasher, jwt)
			}
		})
	}
}

func TestAuthUseCase_RefreshToken(t *testing.T) {
	tests := []struct {
		name    string
		token   string
		setup   func(*mockUserRepository, *mockRefreshTokenRepository, *mockPasswordHasher, *mockJWTService, clock.Clock)
		wantErr bool
		check   func(*testing.T, *usecase.AuthResponse, *mockRefreshTokenRepository, *mockJWTService)
	}{
		{
			name:  "successful refresh",
			token: "valid_refresh_token",
			setup: func(userRepo *mockUserRepository, tokenRepo *mockRefreshTokenRepository, hasher *mockPasswordHasher, jwt *mockJWTService, clock clock.Clock) {
				userRepo.users[1] = &domain.User{
					ID:       1,
					Username: "testuser",
					Role:     domain.RoleAdmin,
					IsActive: true,
				}
				now := clock.Now()
				tokenRepo.tokens["token_hash_123"] = &domain.RefreshToken{
					ID:        1,
					UserID:    1,
					TokenHash: "token_hash_123",
					IssuedAt:  now,
					ExpiresAt: now.Add(7 * 24 * time.Hour),
				}
			},
			wantErr: false,
			check: func(t *testing.T, resp *usecase.AuthResponse, tokenRepo *mockRefreshTokenRepository, jwt *mockJWTService) {
				if resp == nil {
					t.Fatal("expected response, got nil")
				}
				if !tokenRepo.revokeCalled {
					t.Error("expected Revoke to be called")
				}
				if !tokenRepo.createCalled {
					t.Error("expected Create to be called for new token")
				}
			},
		},
		{
			name:  "invalid token",
			token: "invalid_token",
			setup: func(userRepo *mockUserRepository, tokenRepo *mockRefreshTokenRepository, hasher *mockPasswordHasher, jwt *mockJWTService, clock clock.Clock) {
				jwt.validateRefreshTokenErr = domain.NewValidationError("JWT", "", "", "invalid refresh token")
			},
			wantErr: true,
		},
		{
			name:  "user not found",
			token: "valid_refresh_token",
			setup: func(userRepo *mockUserRepository, tokenRepo *mockRefreshTokenRepository, hasher *mockPasswordHasher, jwt *mockJWTService, clock clock.Clock) {
				userRepo.getByIDErr = domain.NewNotFoundError("User", "id", 1, "user not found")
			},
			wantErr: true,
		},
		{
			name:  "user inactive",
			token: "valid_refresh_token",
			setup: func(userRepo *mockUserRepository, tokenRepo *mockRefreshTokenRepository, hasher *mockPasswordHasher, jwt *mockJWTService, clock clock.Clock) {
				userRepo.users[1] = &domain.User{
					ID:       1,
					Username: "testuser",
					Role:     domain.RoleAdmin,
					IsActive: false,
				}
				now := clock.Now()
				tokenRepo.tokens["token_hash_123"] = &domain.RefreshToken{
					ID:        1,
					UserID:    1,
					TokenHash: "token_hash_123",
					IssuedAt:  now,
					ExpiresAt: now.Add(7 * 24 * time.Hour),
				}
			},
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			userRepo := newMockUserRepository()
			tokenRepo := newMockRefreshTokenRepository()
			hasher := newMockPasswordHasher()
			jwt := newMockJWTService()
			clock := mockclock.NewMockClock(time.Now())
			logger := &mockLogger{}
			refreshTTL := 7 * 24 * time.Hour

			tt.setup(userRepo, tokenRepo, hasher, jwt, clock)

			uc := NewAuthUseCase(userRepo, tokenRepo, hasher, jwt, clock, logger, refreshTTL)

			resp, err := uc.RefreshToken(context.Background(), tt.token)

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
				tt.check(t, resp, tokenRepo, jwt)
			}
		})
	}
}

func TestAuthUseCase_Logout(t *testing.T) {
	tests := []struct {
		name    string
		token   string
		setup   func(*mockRefreshTokenRepository, *mockJWTService)
		wantErr bool
		check   func(*testing.T, *mockRefreshTokenRepository)
	}{
		{
			name:  "successful logout",
			token: "valid_refresh_token",
			setup: func(tokenRepo *mockRefreshTokenRepository, jwt *mockJWTService) {
				now := time.Now()
				tokenRepo.tokens["token_hash_123"] = &domain.RefreshToken{
					ID:        1,
					UserID:    1,
					TokenHash: "token_hash_123",
					IssuedAt:  now,
					ExpiresAt: now.Add(7 * 24 * time.Hour),
				}
			},
			wantErr: false,
			check: func(t *testing.T, tokenRepo *mockRefreshTokenRepository) {
				if !tokenRepo.revokeCalled {
					t.Error("expected Revoke to be called")
				}
			},
		},
		{
			name:  "invalid token",
			token: "invalid_token",
			setup: func(tokenRepo *mockRefreshTokenRepository, jwt *mockJWTService) {
				jwt.validateRefreshTokenErr = domain.NewValidationError("JWT", "", "", "invalid refresh token")
			},
			wantErr: true,
		},
		{
			name:  "token not found",
			token: "valid_refresh_token",
			setup: func(tokenRepo *mockRefreshTokenRepository, jwt *mockJWTService) {
			},
			wantErr: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			userRepo := newMockUserRepository()
			tokenRepo := newMockRefreshTokenRepository()
			hasher := newMockPasswordHasher()
			jwt := newMockJWTService()
			clock := mockclock.NewMockClock(time.Now())
			logger := &mockLogger{}
			refreshTTL := 7 * 24 * time.Hour

			tt.setup(tokenRepo, jwt)

			uc := NewAuthUseCase(userRepo, tokenRepo, hasher, jwt, clock, logger, refreshTTL)

			err := uc.Logout(context.Background(), tt.token)

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
				tt.check(t, tokenRepo)
			}
		})
	}
}

func stringPtr(s string) *string {
	return &s
}
