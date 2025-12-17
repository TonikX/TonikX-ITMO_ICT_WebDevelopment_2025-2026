package domain

import "time"

// AcademicYear represents an academic year
type AcademicYear struct {
	ID        int       `json:"id"`
	Name      string    `json:"name"`
	StartDate time.Time `json:"start_date"`
	EndDate   time.Time `json:"end_date"`
	IsCurrent bool      `json:"is_current"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// SubjectType represents a subject type (basic/profile)
type SubjectType struct {
	ID        int       `json:"id"`
	Name      string    `json:"name"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// Gender represents a gender
type Gender struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

// Weekday represents a weekday
type Weekday struct {
	ID       int    `json:"id"`
	Name     string `json:"name"`
	DayOrder int    `json:"day_order"` // 1-7
}

// GradingPeriod represents a grading period (quarter)
type GradingPeriod struct {
	ID             int       `json:"id"`
	AcademicYearID int       `json:"academic_year_id"`
	Name           string    `json:"name"`
	PeriodOrder    int       `json:"period_order"` // 1-4
	StartDate      time.Time `json:"start_date"`
	EndDate        time.Time `json:"end_date"`
	CreatedAt      time.Time `json:"created_at"`
	UpdatedAt      time.Time `json:"updated_at"`
}

// TeacherSubject represents the relationship between teacher and subject
type TeacherSubject struct {
	ID        int        `json:"id"`
	TeacherID int        `json:"teacher_id"`
	SubjectID int        `json:"subject_id"`
	StartDate time.Time  `json:"start_date"`
	EndDate   *time.Time `json:"end_date,omitempty"`
	CreatedAt time.Time  `json:"created_at"`
	UpdatedAt time.Time  `json:"updated_at"`
}
