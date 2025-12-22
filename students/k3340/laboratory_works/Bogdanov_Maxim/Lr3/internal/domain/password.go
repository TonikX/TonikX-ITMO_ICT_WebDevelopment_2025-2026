package domain

// PasswordHasher определяет интерфейс для хеширования паролей
type PasswordHasher interface {
	// Hash хеширует пароль
	Hash(password string) (string, error)

	// Verify проверяет пароль против хеша
	Verify(hashedPassword, password string) error
}
