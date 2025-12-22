package domain

import (
	"time"
)

// UserRole представляет роль пользователя
type UserRole string

const (
	RoleAdmin       UserRole = "admin"
	RoleHeadTeacher UserRole = "head_teacher"
	RoleTeacher     UserRole = "teacher"
)

const (
	MinUsernameLength = 3
	MaxUsernameLength = 50
	MaxEmailLength    = 255
)

// IsValid проверяет, является ли роль валидной
func (r UserRole) IsValid() bool {
	return r == RoleAdmin || r == RoleHeadTeacher || r == RoleTeacher
}

// String возвращает строковое представление роли
func (r UserRole) String() string {
	return string(r)
}

// User представляет пользователя системы
type User struct {
	ID           int
	Username     string
	Email        *string
	PasswordHash string
	Role         UserRole
	TeacherID    *int
	IsActive     bool
	CreatedAt    time.Time
	UpdatedAt    time.Time
	DeletedAt    *time.Time
}

// SetID устанавливает ID пользователя
func (u *User) SetID(id int) {
	u.ID = id
}

// Validate проверяет валидность пользователя
func (u *User) Validate() error {
	if u.Username == "" {
		return NewValidationError("User", "username", u.Username, "username is required")
	}
	if len(u.Username) < MinUsernameLength {
		return NewValidationError("User", "username", u.Username, "username must be at least 3 characters")
	}
	if len(u.Username) > MaxUsernameLength {
		return NewValidationError("User", "username", u.Username, "username must be at most 50 characters")
	}
	if u.Email != nil && *u.Email != "" {
		if len(*u.Email) > MaxEmailLength {
			return NewValidationError("User", "email", *u.Email, "email must be at most 255 characters")
		}
	}
	if u.PasswordHash == "" {
		return NewValidationError("User", "password_hash", "", "password hash is required")
	}
	if !u.Role.IsValid() {
		return NewValidationError("User", "role", u.Role.String(), "invalid role")
	}
	return nil
}

// RefreshToken представляет refresh токен
type RefreshToken struct {
	ID        int
	UserID    int
	TokenHash string
	IssuedAt  time.Time
	ExpiresAt time.Time
	RevokedAt *time.Time
	CreatedAt time.Time
	UpdatedAt time.Time
}

// SetID устанавливает ID токена
func (rt *RefreshToken) SetID(id int) {
	rt.ID = id
}

// IsExpired проверяет, истек ли токен
func (rt *RefreshToken) IsExpired(now time.Time) bool {
	return now.After(rt.ExpiresAt)
}

// IsRevoked проверяет, отозван ли токен
func (rt *RefreshToken) IsRevoked() bool {
	return rt.RevokedAt != nil
}

// IsValid проверяет, валиден ли токен
func (rt *RefreshToken) IsValid(now time.Time) bool {
	return !rt.IsExpired(now) && !rt.IsRevoked()
}
