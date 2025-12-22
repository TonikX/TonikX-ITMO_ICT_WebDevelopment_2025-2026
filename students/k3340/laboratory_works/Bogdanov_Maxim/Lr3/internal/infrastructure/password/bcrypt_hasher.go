package password

import (
	"golang.org/x/crypto/bcrypt"

	"school-service/internal/domain"
)

var _ domain.PasswordHasher = (*BcryptHasher)(nil)

// BcryptHasher реализация PasswordHasher с использованием bcrypt
type BcryptHasher struct {
	cost int
}

// NewBcryptHasher создает новый BcryptHasher
func NewBcryptHasher(cost int) *BcryptHasher {
	if cost == 0 {
		cost = bcrypt.DefaultCost
	}
	return &BcryptHasher{cost: cost}
}

// Hash хеширует пароль
func (h *BcryptHasher) Hash(password string) (string, error) {
	hash, err := bcrypt.GenerateFromPassword([]byte(password), h.cost)
	if err != nil {
		return "", domain.NewError(domain.ErrorCodeInternal, err, "Password", "", "", "failed to hash password", nil)
	}
	return string(hash), nil
}

// Verify проверяет пароль против хеша
func (h *BcryptHasher) Verify(hashedPassword, password string) error {
	err := bcrypt.CompareHashAndPassword([]byte(hashedPassword), []byte(password))
	if err != nil {
		return domain.NewValidationError("Password", "", "", "invalid password")
	}
	return nil
}
