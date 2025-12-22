package domain

import (
	"fmt"
	"time"

	"school-service/internal/domain/clock"
)

const (
	entityClass = "Class"
)

// Class представляет сущность класса
type Class struct {
	id             int
	grade          int
	letter         string
	academicYearID int
	classTeacherID *int
	createdAt      time.Time
	updatedAt      time.Time
	deletedAt      *time.Time
}

// NewClass создает новый экземпляр Class
func NewClass(clock clock.Clock, grade int, letter string, academicYearID int, classTeacherID *int) (*Class, error) {
	now := clock.Now()
	class := &Class{
		grade:          grade,
		letter:         letter,
		academicYearID: academicYearID,
		classTeacherID: classTeacherID,
		createdAt:      now,
		updatedAt:      now,
	}
	if err := class.Validate(); err != nil {
		return nil, err
	}
	return class, nil
}

// RestoreClassFromDB восстанавливает Class из данных БД
func RestoreClassFromDB(id, grade int, letter string, academicYearID int, classTeacherID *int, createdAt, updatedAt time.Time, deletedAt *time.Time) *Class {
	return &Class{
		id:             id,
		grade:          grade,
		letter:         letter,
		academicYearID: academicYearID,
		classTeacherID: classTeacherID,
		createdAt:      createdAt,
		updatedAt:      updatedAt,
		deletedAt:      deletedAt,
	}
}

// ID возвращает идентификатор класса
func (c *Class) ID() int {
	return c.id
}

// SetID устанавливает идентификатор (используется только при создании в БД)
func (c *Class) SetID(id int) {
	c.id = id
}

// Grade возвращает номер класса
func (c *Class) Grade() int {
	return c.grade
}

// SetGrade устанавливает номер класса
func (c *Class) SetGrade(clock clock.Clock, grade int) {
	c.grade = grade
	c.updatedAt = clock.Now()
}

// Letter возвращает букву класса
func (c *Class) Letter() string {
	return c.letter
}

// SetLetter устанавливает букву класса
func (c *Class) SetLetter(clock clock.Clock, letter string) {
	c.letter = letter
	c.updatedAt = clock.Now()
}

// AcademicYearID возвращает идентификатор учебного года
func (c *Class) AcademicYearID() int {
	return c.academicYearID
}

// SetAcademicYearID устанавливает идентификатор учебного года
func (c *Class) SetAcademicYearID(clock clock.Clock, academicYearID int) {
	c.academicYearID = academicYearID
	c.updatedAt = clock.Now()
}

// ClassTeacherID возвращает идентификатор классного руководителя
func (c *Class) ClassTeacherID() *int {
	return c.classTeacherID
}

// SetClassTeacherID устанавливает идентификатор классного руководителя
func (c *Class) SetClassTeacherID(clock clock.Clock, classTeacherID *int) {
	c.classTeacherID = classTeacherID
	c.updatedAt = clock.Now()
}

// CreatedAt возвращает время создания
func (c *Class) CreatedAt() time.Time {
	return c.createdAt
}

// UpdatedAt возвращает время обновления
func (c *Class) UpdatedAt() time.Time {
	return c.updatedAt
}

// DeletedAt возвращает время удаления
func (c *Class) DeletedAt() *time.Time {
	return c.deletedAt
}

// IsDeleted проверяет, удален ли класс (soft delete)
func (c *Class) IsDeleted() bool {
	return c.deletedAt != nil
}

// MarkAsDeleted помечает класс как удаленный
func (c *Class) MarkAsDeleted(clock clock.Clock) {
	now := clock.Now()
	c.deletedAt = &now
	c.updatedAt = now
}

// FullName возвращает полное название класса (например, "9А")
func (c *Class) FullName() string {
	return fmt.Sprintf("%d%s", c.grade, c.letter)
}

const (
	minClassGrade        = 1
	maxClassGrade        = 11
	maxClassLetterLength = 5
)

// Validate проверяет валидность данных класса
func (c *Class) Validate() error {
	if c.grade < minClassGrade || c.grade > maxClassGrade {
		return NewValidationError(entityClass, "grade", c.grade, fmt.Sprintf("must be between %d and %d", minClassGrade, maxClassGrade))
	}
	if c.letter == "" {
		return NewValidationError(entityClass, "letter", c.letter, "cannot be empty")
	}
	if len(c.letter) > maxClassLetterLength {
		return NewValidationError(entityClass, "letter", c.letter, fmt.Sprintf("length must be <= %d", maxClassLetterLength))
	}
	if c.academicYearID <= 0 {
		return NewValidationError(entityClass, "academicYearID", c.academicYearID, "must be > 0")
	}
	return nil
}
