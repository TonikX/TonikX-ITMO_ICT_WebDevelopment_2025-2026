package jwt

import (
	"encoding/hex"
	"errors"
	"fmt"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"golang.org/x/crypto/sha3"

	"school-service/internal/domain"
	"school-service/internal/domain/clock"
)

var _ domain.JWTService = (*JWTService)(nil)

// JWTService реализация JWTService
type JWTService struct {
	accessSecret     []byte
	refreshSecret    []byte
	accessTTL        time.Duration
	refreshTTL       time.Duration
	clock            clock.Clock
	refreshTokenSalt string
}

// JWTConfig конфигурация для JWT сервиса
type JWTConfig struct {
	AccessSecret  string
	RefreshSecret string
	AccessTTL     time.Duration
	RefreshTTL    time.Duration
	Clock         clock.Clock
}

// NewJWTService создает новый JWT сервис
func NewJWTService(cfg JWTConfig) *JWTService {
	return &JWTService{
		accessSecret:     []byte(cfg.AccessSecret),
		refreshSecret:    []byte(cfg.RefreshSecret),
		accessTTL:        cfg.AccessTTL,
		refreshTTL:       cfg.RefreshTTL,
		clock:            cfg.Clock,
		refreshTokenSalt: cfg.RefreshSecret,
	}
}

// accessClaims представляет claims для access токена
type accessClaims struct {
	UserID   int    `json:"user_id"`
	Username string `json:"username"`
	Role     string `json:"role"`
	jwt.RegisteredClaims
}

// refreshClaims представляет claims для refresh токена
type refreshClaims struct {
	UserID int `json:"user_id"`
	jwt.RegisteredClaims
}

// GenerateAccessToken генерирует access токен
func (s *JWTService) GenerateAccessToken(userID int, username string, role domain.UserRole) (string, error) {
	now := s.clock.Now()
	claims := accessClaims{
		UserID:   userID,
		Username: username,
		Role:     role.String(),
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(now.Add(s.accessTTL)),
			IssuedAt:  jwt.NewNumericDate(now),
			NotBefore: jwt.NewNumericDate(now),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString(s.accessSecret)
	if err != nil {
		return "", domain.NewError(domain.ErrorCodeInternal, err, "JWT", "", "", "failed to generate access token", nil)
	}

	return tokenString, nil
}

func (s *JWTService) GenerateRefreshToken(userID int) (string, string, error) {
	now := s.clock.Now()
	claims := refreshClaims{
		UserID: userID,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(now.Add(s.refreshTTL)),
			IssuedAt:  jwt.NewNumericDate(now),
			NotBefore: jwt.NewNumericDate(now),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString(s.refreshSecret)
	if err != nil {
		return "", "", domain.NewError(domain.ErrorCodeInternal, err, "JWT", "", "", "failed to generate refresh token", nil)
	}

	tokenHash := s.hashToken(tokenString)

	return tokenString, tokenHash, nil
}

func (s *JWTService) HashRefreshToken(token string) string {
	return s.hashToken(token)
}

func (s *JWTService) hashToken(token string) string {
	h := sha3.New256()
	h.Write([]byte(token))
	h.Write([]byte(s.refreshTokenSalt))
	return hex.EncodeToString(h.Sum(nil))
}

func (s *JWTService) ValidateAccessToken(tokenString string) (*domain.TokenClaims, error) {
	token, err := jwt.ParseWithClaims(tokenString, &accessClaims{}, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return s.accessSecret, nil
	})

	if err != nil {
		if errors.Is(err, jwt.ErrTokenExpired) {
			return nil, domain.NewValidationError("JWT", "", "", "access token expired")
		}
		return nil, domain.NewValidationError("JWT", "", "", "invalid access token")
	}

	claims, ok := token.Claims.(*accessClaims)
	if !ok || !token.Valid {
		return nil, domain.NewValidationError("JWT", "", "", "invalid access token")
	}

	role := domain.UserRole(claims.Role)
	if !role.IsValid() {
		return nil, domain.NewValidationError("JWT", "", "", "invalid role in token")
	}

	expiresAt := time.Time{}
	if claims.ExpiresAt != nil {
		expiresAt = claims.ExpiresAt.Time
	}

	return &domain.TokenClaims{
		UserID:    claims.UserID,
		Username:  claims.Username,
		Role:      role,
		ExpiresAt: expiresAt,
	}, nil
}

func (s *JWTService) ValidateRefreshToken(tokenString string) (*domain.TokenClaims, error) {
	token, err := jwt.ParseWithClaims(tokenString, &refreshClaims{}, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return s.refreshSecret, nil
	})

	if err != nil {
		if errors.Is(err, jwt.ErrTokenExpired) {
			return nil, domain.NewValidationError("JWT", "", "", "refresh token expired")
		}
		return nil, domain.NewValidationError("JWT", "", "", "invalid refresh token")
	}

	claims, ok := token.Claims.(*refreshClaims)
	if !ok || !token.Valid {
		return nil, domain.NewValidationError("JWT", "", "", "invalid refresh token")
	}

	expiresAt := time.Time{}
	if claims.ExpiresAt != nil {
		expiresAt = claims.ExpiresAt.Time
	}

	return &domain.TokenClaims{
		UserID:    claims.UserID,
		ExpiresAt: expiresAt,
	}, nil
}
