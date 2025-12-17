package clock

import "time"

// Clock предоставляет абстракцию для работы со временем
type Clock interface {
	Now() time.Time
	Since(t time.Time) time.Duration
	NewTicker(d time.Duration) Ticker
}

// Ticker предоставляет абстракцию для тикера
type Ticker interface {
	C() <-chan time.Time
	Stop()
}
