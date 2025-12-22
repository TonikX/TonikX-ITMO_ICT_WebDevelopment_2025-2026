package health

import "context"

// HealthChecker интерфейс для проверки здоровья компонента
type HealthChecker interface {
	Health(ctx context.Context) error
}
