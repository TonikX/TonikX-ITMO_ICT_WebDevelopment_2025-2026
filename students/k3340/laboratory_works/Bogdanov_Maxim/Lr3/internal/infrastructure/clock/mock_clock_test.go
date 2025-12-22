package clock

import (
	"testing"
	"time"
)

func TestMockClock_Now(t *testing.T) {
	now := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	clock := NewMockClock(now)

	if clock.Now() != now {
		t.Errorf("expected Now() = %v, got %v", now, clock.Now())
	}
}

func TestMockClock_SetNow(t *testing.T) {
	now1 := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	clock := NewMockClock(now1)

	now2 := time.Date(2024, 1, 1, 13, 0, 0, 0, time.UTC)
	clock.SetNow(now2)

	if clock.Now() != now2 {
		t.Errorf("expected Now() = %v, got %v", now2, clock.Now())
	}
}

func TestMockClock_Advance(t *testing.T) {
	now := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	clock := NewMockClock(now)

	clock.Advance(2 * time.Hour)
	expected := time.Date(2024, 1, 1, 14, 0, 0, 0, time.UTC)

	if clock.Now() != expected {
		t.Errorf("expected Now() = %v, got %v", expected, clock.Now())
	}
}

func TestMockClock_Since(t *testing.T) {
	now := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	clock := NewMockClock(now)

	past := time.Date(2024, 1, 1, 11, 0, 0, 0, time.UTC)
	duration := clock.Since(past)
	expected := 1 * time.Hour

	if duration != expected {
		t.Errorf("expected Since() = %v, got %v", expected, duration)
	}
}

func TestMockClock_Sleep(t *testing.T) {
	clock := NewMockClock(time.Now())

	clock.Sleep(100 * time.Millisecond)
	clock.Sleep(200 * time.Millisecond)

	sleeps := clock.GetSleeps()
	if len(sleeps) != 2 {
		t.Errorf("expected 2 sleeps, got %d", len(sleeps))
	}
	if sleeps[0] != 100*time.Millisecond {
		t.Errorf("expected first sleep = 100ms, got %v", sleeps[0])
	}
	if sleeps[1] != 200*time.Millisecond {
		t.Errorf("expected second sleep = 200ms, got %v", sleeps[1])
	}
}

func TestMockClock_NewTicker(t *testing.T) {
	clock := NewMockClock(time.Now())
	ticker := clock.NewTicker(100 * time.Millisecond)

	if ticker == nil {
		t.Fatal("expected non-nil ticker")
	}

	select {
	case <-ticker.C():
		t.Error("expected no tick before TickAll()")
	default:
		// Ожидаемое поведение
	}
}

func TestMockClock_TickAll(t *testing.T) {
	now := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	clock := NewMockClock(now)

	ticker1 := clock.NewTicker(100 * time.Millisecond)
	ticker2 := clock.NewTicker(200 * time.Millisecond)

	clock.TickAll()

	select {
	case tick := <-ticker1.C():
		if !tick.Equal(now) {
			t.Errorf("expected tick = %v, got %v", now, tick)
		}
	case <-time.After(10 * time.Millisecond):
		t.Error("expected tick from ticker1")
	}

	select {
	case tick := <-ticker2.C():
		if !tick.Equal(now) {
			t.Errorf("expected tick = %v, got %v", now, tick)
		}
	case <-time.After(10 * time.Millisecond):
		t.Error("expected tick from ticker2")
	}
}

func TestMockTicker_Stop(t *testing.T) {
	clock := NewMockClock(time.Now())
	ticker := clock.NewTicker(100 * time.Millisecond)

	clock.TickAll()

	select {
	case <-ticker.C():
		// Получили тик до остановки
	default:
		t.Error("expected tick before Stop()")
	}

	ticker.Stop()

	clock.TickAll()

	select {
	case _, ok := <-ticker.C():
		if ok {
			t.Error("expected no ticks after Stop()")
		}
		// ok == false означает, что канал закрыт - это ожидаемое поведение
	default:
		// Канал закрыт, нет значений - это тоже нормально
	}
}

func TestMockTicker_MultipleTicks(t *testing.T) {
	now1 := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
	clock := NewMockClock(now1)

	ticker := clock.NewTicker(100 * time.Millisecond)

	clock.TickAll()

	select {
	case tick := <-ticker.C():
		if !tick.Equal(now1) {
			t.Errorf("expected first tick = %v, got %v", now1, tick)
		}
	case <-time.After(10 * time.Millisecond):
		t.Error("expected first tick")
	}

	now2 := time.Date(2024, 1, 1, 12, 1, 0, 0, time.UTC)
	clock.SetNow(now2)
	clock.TickAll()

	select {
	case tick := <-ticker.C():
		if !tick.Equal(now2) {
			t.Errorf("expected second tick = %v, got %v", now2, tick)
		}
	case <-time.After(10 * time.Millisecond):
		t.Error("expected second tick")
	}
}
