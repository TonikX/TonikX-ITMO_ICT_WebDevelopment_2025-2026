package clock

import (
	"time"

	"school-service/internal/domain/clock"
)

var _ clock.Clock = (*MockClock)(nil)

// MockClock реализация Clock для тестирования
type MockClock struct {
	now     time.Time
	tickers []*mockTicker
	sleeps  []time.Duration
}

// NewMockClock создает новый экземпляр MockClock
func NewMockClock(now time.Time) *MockClock {
	return &MockClock{
		now:     now,
		tickers: make([]*mockTicker, 0),
		sleeps:  make([]time.Duration, 0),
	}
}

// Now возвращает установленное время
func (m *MockClock) Now() time.Time {
	return m.now
}

// SetNow устанавливает текущее время для мока
func (m *MockClock) SetNow(now time.Time) {
	m.now = now
}

// Advance увеличивает время на указанную длительность
func (m *MockClock) Advance(d time.Duration) {
	m.now = m.now.Add(d)
}

// Since возвращает время, прошедшее с момента t
func (m *MockClock) Since(t time.Time) time.Duration {
	return m.now.Sub(t)
}

// Sleep записывает длительность сна (для проверки в тестах)
func (m *MockClock) Sleep(d time.Duration) {
	m.sleeps = append(m.sleeps, d)
}

// GetSleeps возвращает все зафиксированные вызовы Sleep
func (m *MockClock) GetSleeps() []time.Duration {
	return m.sleeps
}

// NewTicker создает новый мок-тикер
func (m *MockClock) NewTicker(d time.Duration) clock.Ticker {
	ticker := &mockTicker{
		duration: d,
		c:        make(chan time.Time, 1),
		stopped:  false,
	}
	m.tickers = append(m.tickers, ticker)
	return ticker
}

// TickAll отправляет тик во все активные тикеры
func (m *MockClock) TickAll() {
	for _, ticker := range m.tickers {
		if !ticker.stopped {
			select {
			case ticker.c <- m.now:
			default:
			}
		}
	}
}

var _ clock.Ticker = (*mockTicker)(nil)

// mockTicker обертка над тикером для тестирования
type mockTicker struct {
	duration time.Duration
	c        chan time.Time
	stopped  bool
}

// C возвращает канал, в который отправляются тики
func (m *mockTicker) C() <-chan time.Time {
	return m.c
}

// Stop останавливает тикер
func (m *mockTicker) Stop() {
	m.stopped = true
	close(m.c)
}
