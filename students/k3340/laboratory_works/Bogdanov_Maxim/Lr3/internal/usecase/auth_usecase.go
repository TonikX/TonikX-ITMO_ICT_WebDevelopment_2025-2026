package usecase

import (
	"context"
	"time"

	"school-service/internal/domain"
	"school-service/internal/domain/clock"
	"school-service/internal/domain/logger"
	"school-service/internal/domain/repository"
	"school-service/internal/domain/usecase"
)

var _ usecase.AuthUseCase = (*AuthUseCase)(nil)

type AuthUseCase struct {
	userRepo         repository.UserRepository
	refreshTokenRepo repository.RefreshTokenRepository
	passwordHasher   domain.PasswordHasher
	jwtService       domain.JWTService
	clock            clock.Clock
	logger           logger.Logger
	refreshTokenTTL  time.Duration
}

func NewAuthUseCase(
	userRepo repository.UserRepository,
	refreshTokenRepo repository.RefreshTokenRepository,
	passwordHasher domain.PasswordHasher,
	jwtService domain.JWTService,
	clock clock.Clock,
	logger logger.Logger,
	refreshTokenTTL time.Duration,
) *AuthUseCase {
	return &AuthUseCase{
		userRepo:         userRepo,
		refreshTokenRepo: refreshTokenRepo,
		passwordHasher:   passwordHasher,
		jwtService:       jwtService,
		clock:            clock,
		logger:           logger,
		refreshTokenTTL:  refreshTokenTTL,
	}
}

// Register регистрирует нового пользователя
func (uc *AuthUseCase) Register(ctx context.Context, req *usecase.RegisterRequest) (*usecase.AuthResponse, error) {
	_, err := uc.userRepo.GetByUsername(ctx, req.Username)
	if err == nil {
		return nil, domain.NewAlreadyExistsError("User", "username", req.Username, "user with this username already exists")
	}
	if !domain.IsNotFound(err) {
		uc.logger.WithError(err).Error("failed to check username existence")
		return nil, err
	}

	if req.Email != nil && *req.Email != "" {
		_, err = uc.userRepo.GetByEmail(ctx, *req.Email)
		if err == nil {
			return nil, domain.NewAlreadyExistsError("User", "email", *req.Email, "user with this email already exists")
		}
		if !domain.IsNotFound(err) {
			uc.logger.WithError(err).Error("failed to check email existence")
			return nil, err
		}
	}

	if !req.Role.IsValid() {
		return nil, domain.NewValidationError("User", "role", req.Role.String(), "invalid role")
	}

	passwordHash, err := uc.passwordHasher.Hash(req.Password)
	if err != nil {
		uc.logger.WithError(err).Error("failed to hash password")
		return nil, err
	}

	user := &domain.User{
		Username:     req.Username,
		Email:        req.Email,
		PasswordHash: passwordHash,
		Role:         req.Role,
		TeacherID:    req.TeacherID,
		IsActive:     true,
	}

	if err := user.Validate(); err != nil {
		return nil, err
	}

	if err := uc.userRepo.Create(ctx, user); err != nil {
		uc.logger.WithError(err).Error("failed to create user")
		return nil, err
	}

	accessToken, err := uc.jwtService.GenerateAccessToken(user.ID, user.Username, user.Role)
	if err != nil {
		uc.logger.WithError(err).Error("failed to generate access token")
		return nil, err
	}

	refreshToken, tokenHash, err := uc.jwtService.GenerateRefreshToken(user.ID)
	if err != nil {
		uc.logger.WithError(err).Error("failed to generate refresh token")
		return nil, err
	}

	now := uc.clock.Now()
	refreshTokenEntity := &domain.RefreshToken{
		UserID:    user.ID,
		TokenHash: tokenHash,
		IssuedAt:  now,
		ExpiresAt: now.Add(uc.refreshTokenTTL),
	}

	if err := uc.refreshTokenRepo.Create(ctx, refreshTokenEntity); err != nil {
		uc.logger.WithError(err).Error("failed to save refresh token")
		return nil, err
	}

	return &usecase.AuthResponse{
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
		User: &usecase.UserResponse{
			ID:        user.ID,
			Username:  user.Username,
			Email:     user.Email,
			Role:      user.Role,
			TeacherID: user.TeacherID,
		},
	}, nil
}

// Login выполняет вход пользователя
func (uc *AuthUseCase) Login(ctx context.Context, req *usecase.LoginRequest) (*usecase.AuthResponse, error) {
	user, err := uc.userRepo.GetByUsername(ctx, req.Username)
	if err != nil {
		if domain.IsNotFound(err) {
			return nil, domain.NewValidationError("User", "username", req.Username, "invalid username or password")
		}
		uc.logger.WithError(err).Error("failed to get user")
		return nil, err
	}

	if err := uc.passwordHasher.Verify(user.PasswordHash, req.Password); err != nil {
		return nil, domain.NewValidationError("User", "password", "", "invalid username or password")
	}

	accessToken, err := uc.jwtService.GenerateAccessToken(user.ID, user.Username, user.Role)
	if err != nil {
		uc.logger.WithError(err).Error("failed to generate access token")
		return nil, err
	}

	refreshToken, tokenHash, err := uc.jwtService.GenerateRefreshToken(user.ID)
	if err != nil {
		uc.logger.WithError(err).Error("failed to generate refresh token")
		return nil, err
	}

	now := uc.clock.Now()
	refreshTokenEntity := &domain.RefreshToken{
		UserID:    user.ID,
		TokenHash: tokenHash,
		IssuedAt:  now,
		ExpiresAt: now.Add(uc.refreshTokenTTL),
	}

	if err := uc.refreshTokenRepo.Create(ctx, refreshTokenEntity); err != nil {
		uc.logger.WithError(err).Error("failed to save refresh token")
		return nil, err
	}

	return &usecase.AuthResponse{
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
		User: &usecase.UserResponse{
			ID:        user.ID,
			Username:  user.Username,
			Email:     user.Email,
			Role:      user.Role,
			TeacherID: user.TeacherID,
		},
	}, nil
}

// RefreshToken обновляет access токен используя refresh токен
func (uc *AuthUseCase) RefreshToken(ctx context.Context, refreshToken string) (*usecase.AuthResponse, error) {
	claims, err := uc.jwtService.ValidateRefreshToken(refreshToken)
	if err != nil {
		return nil, err
	}

	user, err := uc.userRepo.GetByID(ctx, claims.UserID)
	if err != nil {
		uc.logger.WithError(err).Error("failed to get user")
		return nil, err
	}

	if !user.IsActive {
		return nil, domain.NewValidationError("User", "is_active", false, "user is not active")
	}

	tokenHash := uc.jwtService.HashRefreshToken(refreshToken)
	tokenEntity, err := uc.refreshTokenRepo.GetByTokenHash(ctx, tokenHash)
	if err != nil {
		if domain.IsNotFound(err) {
			return nil, domain.NewValidationError("RefreshToken", "token", "", "refresh token not found")
		}
		uc.logger.WithError(err).Error("failed to get refresh token")
		return nil, err
	}

	now := uc.clock.Now()
	if !tokenEntity.IsValid(now) {
		return nil, domain.NewValidationError("RefreshToken", "token", "", "refresh token expired or revoked")
	}

	accessToken, err := uc.jwtService.GenerateAccessToken(user.ID, user.Username, user.Role)
	if err != nil {
		uc.logger.WithError(err).Error("failed to generate access token")
		return nil, err
	}

	newRefreshToken, newTokenHash, err := uc.jwtService.GenerateRefreshToken(user.ID)
	if err != nil {
		uc.logger.WithError(err).Error("failed to generate refresh token")
		return nil, err
	}

	if err := uc.refreshTokenRepo.Revoke(ctx, tokenHash); err != nil {
		uc.logger.WithError(err).Error("failed to revoke old refresh token")
	}

	newRefreshTokenEntity := &domain.RefreshToken{
		UserID:    user.ID,
		TokenHash: newTokenHash,
		IssuedAt:  now,
		ExpiresAt: now.Add(uc.refreshTokenTTL),
	}

	if err := uc.refreshTokenRepo.Create(ctx, newRefreshTokenEntity); err != nil {
		uc.logger.WithError(err).Error("failed to save new refresh token")
		return nil, err
	}

	return &usecase.AuthResponse{
		AccessToken:  accessToken,
		RefreshToken: newRefreshToken,
		User: &usecase.UserResponse{
			ID:        user.ID,
			Username:  user.Username,
			Email:     user.Email,
			Role:      user.Role,
			TeacherID: user.TeacherID,
		},
	}, nil
}

func (uc *AuthUseCase) Logout(ctx context.Context, refreshToken string) error {
	_, err := uc.jwtService.ValidateRefreshToken(refreshToken)
	if err != nil {
		return err
	}

	tokenHash := uc.jwtService.HashRefreshToken(refreshToken)
	if err := uc.refreshTokenRepo.Revoke(ctx, tokenHash); err != nil {
		if domain.IsNotFound(err) {
			return nil
		}
		uc.logger.WithError(err).Error("failed to revoke refresh token")
		return err
	}

	return nil
}
