package clock

import (
	"testing"
	"time"
)

func TestRealClock_Now(t *testing.T) {
	clock := NewRealClock()
	now1 := clock.Now()
	time.Sleep(10 * time.Millisecond)
	now2 := clock.Now()

	if now2.Before(now1) {
		t.Errorf("expected now2 to be after now1")
	}

	// Проверяем, что время возвращается в UTC
	if now1.Location() != time.UTC {
		t.Errorf("expected time to be in UTC, got %v", now1.Location())
	}
	if now2.Location() != time.UTC {
		t.Errorf("expected time to be in UTC, got %v", now2.Location())
	}
}

func TestRealClock_Since(t *testing.T) {
	clock := NewRealClock()
	start := clock.Now()
	time.Sleep(50 * time.Millisecond)
	duration := clock.Since(start)

	if duration < 50*time.Millisecond {
		t.Errorf("expected duration >= 50ms, got %v", duration)
	}
	if duration > 200*time.Millisecond {
		t.Errorf("expected duration < 200ms, got %v", duration)
	}
}

func TestRealClock_NewTicker(t *testing.T) {
	clock := NewRealClock()
	ticker := clock.NewTicker(100 * time.Millisecond)
	defer ticker.Stop()

	if ticker == nil {
		t.Fatal("expected non-nil ticker")
	}

	select {
	case <-ticker.C():
		// Ticker работает
	case <-time.After(200 * time.Millisecond):
		t.Error("expected tick within 200ms")
	}
}

func TestRealTicker_Stop(t *testing.T) {
	clock := NewRealClock()
	ticker := clock.NewTicker(10 * time.Millisecond)
	ticker.Stop()

	select {
	case <-ticker.C():
		t.Error("expected no ticks after Stop()")
	case <-time.After(50 * time.Millisecond):
		// Ожидаемое поведение - нет тиков после остановки
	}
}
