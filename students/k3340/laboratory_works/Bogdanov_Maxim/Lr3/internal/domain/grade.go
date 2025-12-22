package domain

import (
	"fmt"
	"time"

	"school-service/internal/domain/clock"
)

const (
	entityGrade = "Grade"
	minGrade    = 1
	maxGrade    = 5
)

// Grade представляет оценку ученика
type Grade struct {
	id              int
	studentID       int
	subjectID       int
	gradingPeriodID int
	grade           int
	createdAt       time.Time
	updatedAt       time.Time
}

// NewGrade создает новый экземпляр Grade
func NewGrade(clock clock.Clock, studentID, subjectID, gradingPeriodID, grade int) (*Grade, error) {
	now := clock.Now()
	gradeEntity := &Grade{
		studentID:       studentID,
		subjectID:       subjectID,
		gradingPeriodID: gradingPeriodID,
		grade:           grade,
		createdAt:       now,
		updatedAt:       now,
	}
	if err := gradeEntity.Validate(); err != nil {
		return nil, err
	}
	return gradeEntity, nil
}

// RestoreGradeFromDB восстанавливает Grade из данных БД
func RestoreGradeFromDB(id, studentID, subjectID, gradingPeriodID, grade int, createdAt, updatedAt time.Time) *Grade {
	return &Grade{
		id:              id,
		studentID:       studentID,
		subjectID:       subjectID,
		gradingPeriodID: gradingPeriodID,
		grade:           grade,
		createdAt:       createdAt,
		updatedAt:       updatedAt,
	}
}

// ID возвращает идентификатор оценки
func (g *Grade) ID() int {
	return g.id
}

// SetID устанавливает идентификатор (используется только при создании в БД)
func (g *Grade) SetID(id int) {
	g.id = id
}

// StudentID возвращает идентификатор ученика
func (g *Grade) StudentID() int {
	return g.studentID
}

// SetStudentID устанавливает идентификатор ученика
func (g *Grade) SetStudentID(clock clock.Clock, studentID int) {
	g.studentID = studentID
	g.updatedAt = clock.Now()
}

// SubjectID возвращает идентификатор предмета
func (g *Grade) SubjectID() int {
	return g.subjectID
}

// SetSubjectID устанавливает идентификатор предмета
func (g *Grade) SetSubjectID(clock clock.Clock, subjectID int) {
	g.subjectID = subjectID
	g.updatedAt = clock.Now()
}

// GradingPeriodID возвращает идентификатор оценочного периода
func (g *Grade) GradingPeriodID() int {
	return g.gradingPeriodID
}

// SetGradingPeriodID устанавливает идентификатор оценочного периода
func (g *Grade) SetGradingPeriodID(clock clock.Clock, gradingPeriodID int) {
	g.gradingPeriodID = gradingPeriodID
	g.updatedAt = clock.Now()
}

// Grade возвращает оценку
func (g *Grade) Grade() int {
	return g.grade
}

// SetGrade устанавливает оценку
func (g *Grade) SetGrade(clock clock.Clock, grade int) error {
	g.grade = grade
	g.updatedAt = clock.Now()
	return g.Validate()
}

// CreatedAt возвращает время создания
func (g *Grade) CreatedAt() time.Time {
	return g.createdAt
}

// UpdatedAt возвращает время обновления
func (g *Grade) UpdatedAt() time.Time {
	return g.updatedAt
}

// Validate проверяет валидность данных оценки
func (g *Grade) Validate() error {
	if g.grade < minGrade || g.grade > maxGrade {
		return NewValidationError(entityGrade, "grade", g.grade, fmt.Sprintf("must be between %d and %d", minGrade, maxGrade))
	}
	if g.studentID <= 0 {
		return NewValidationError(entityGrade, "studentID", g.studentID, "must be > 0")
	}
	if g.subjectID <= 0 {
		return NewValidationError(entityGrade, "subjectID", g.subjectID, "must be > 0")
	}
	if g.gradingPeriodID <= 0 {
		return NewValidationError(entityGrade, "gradingPeriodID", g.gradingPeriodID, "must be > 0")
	}
	return nil
}
