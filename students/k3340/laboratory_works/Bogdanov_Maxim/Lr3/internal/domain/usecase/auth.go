package usecase

import (
	"context"

	"school-service/internal/domain"
)

// AuthUseCase определяет интерфейс для аутентификации и авторизации
type AuthUseCase interface {
	// Register регистрирует нового пользователя
	Register(ctx context.Context, req *RegisterRequest) (*AuthResponse, error)

	// Login выполняет вход пользователя
	Login(ctx context.Context, req *LoginRequest) (*AuthResponse, error)

	// RefreshToken обновляет access токен используя refresh токен
	RefreshToken(ctx context.Context, refreshToken string) (*AuthResponse, error)

	// Logout выполняет выход пользователя (отзывает refresh токен)
	Logout(ctx context.Context, refreshToken string) error
}

// RegisterRequest запрос на регистрацию
type RegisterRequest struct {
	Username  string
	Email     *string
	Password  string
	Role      domain.UserRole
	TeacherID *int
}

// LoginRequest запрос на вход
type LoginRequest struct {
	Username string
	Password string
}

// AuthResponse ответ с токенами
type AuthResponse struct {
	AccessToken  string
	RefreshToken string
	User         *UserResponse
}

// UserResponse информация о пользователе
type UserResponse struct {
	ID        int
	Username  string
	Email     *string
	Role      domain.UserRole
	TeacherID *int
}
