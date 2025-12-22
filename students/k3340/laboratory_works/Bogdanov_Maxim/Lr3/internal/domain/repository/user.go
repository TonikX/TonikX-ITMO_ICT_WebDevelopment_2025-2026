package repository

import (
	"context"
	"time"

	"school-service/internal/domain"
)

// UserRepository определяет интерфейс для работы с пользователями
type UserRepository interface {
	// Create создает нового пользователя
	Create(ctx context.Context, user *domain.User) error

	// GetByID получает пользователя по ID
	GetByID(ctx context.Context, id int) (*domain.User, error)

	// GetByUsername получает пользователя по username
	GetByUsername(ctx context.Context, username string) (*domain.User, error)

	// GetByEmail получает пользователя по email
	GetByEmail(ctx context.Context, email string) (*domain.User, error)

	// Update обновляет пользователя
	Update(ctx context.Context, user *domain.User) error

	// Delete выполняет soft delete пользователя
	Delete(ctx context.Context, id int) error
}

// RefreshTokenRepository определяет интерфейс для работы с refresh токенами
type RefreshTokenRepository interface {
	// Create создает новый refresh токен
	Create(ctx context.Context, token *domain.RefreshToken) error

	// GetByTokenHash получает токен по хешу
	GetByTokenHash(ctx context.Context, tokenHash string) (*domain.RefreshToken, error)

	// GetByUserID получает все активные токены пользователя
	GetByUserID(ctx context.Context, userID int) ([]*domain.RefreshToken, error)

	// Revoke отзывает токен
	Revoke(ctx context.Context, tokenHash string) error

	// RevokeAllForUser отзывает все токены пользователя
	RevokeAllForUser(ctx context.Context, userID int) error

	// DeleteExpired удаляет истекшие токены
	DeleteExpired(ctx context.Context, before time.Time) error
}
