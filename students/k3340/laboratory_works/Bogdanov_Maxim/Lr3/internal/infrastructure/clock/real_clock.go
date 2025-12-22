package clock

import (
	"time"

	"school-service/internal/domain/clock"
)

var _ clock.Clock = (*RealClock)(nil)

// RealClock реализация Clock, использующая реальное время
type RealClock struct{}

// NewRealClock создает новый экземпляр RealClock
func NewRealClock() *RealClock {
	return &RealClock{}
}

// Now возвращает текущее время в UTC
func (r *RealClock) Now() time.Time {
	return time.Now().UTC()
}

// Since возвращает время, прошедшее с момента t
func (r *RealClock) Since(t time.Time) time.Duration {
	return time.Since(t)
}

// NewTicker создает новый тикер с указанным интервалом
func (r *RealClock) NewTicker(d time.Duration) clock.Ticker {
	return &realTicker{ticker: time.NewTicker(d)}
}

var _ clock.Ticker = (*realTicker)(nil)

// realTicker обертка над time.Ticker
type realTicker struct {
	ticker *time.Ticker
}

// C возвращает канал, в который отправляются тики
func (r *realTicker) C() <-chan time.Time {
	return r.ticker.C
}

// Stop останавливает тикер
func (r *realTicker) Stop() {
	r.ticker.Stop()
}
