package domain

import (
	"time"
)

// JWTService определяет интерфейс для работы с JWT токенами
type JWTService interface {
	// GenerateAccessToken генерирует access токен
	GenerateAccessToken(userID int, username string, role UserRole) (string, error)

	// GenerateRefreshToken генерирует refresh токен
	GenerateRefreshToken(userID int) (string, string, error) // возвращает токен и его хеш

	// HashRefreshToken хеширует refresh токен для хранения в БД
	HashRefreshToken(token string) string

	// ValidateAccessToken валидирует access токен
	ValidateAccessToken(tokenString string) (*TokenClaims, error)

	// ValidateRefreshToken валидирует refresh токен
	ValidateRefreshToken(tokenString string) (*TokenClaims, error)
}

// TokenClaims представляет claims JWT токена
type TokenClaims struct {
	UserID    int
	Username  string
	Role      UserRole
	ExpiresAt time.Time
}
