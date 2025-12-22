package domain

import (
	"fmt"
	"time"

	"school-service/internal/domain/clock"
)

const (
	entityTeacher = "Teacher"
)

// Teacher представляет сущность учителя
type Teacher struct {
	id          int
	firstName   string
	lastName    string
	middleName  *string
	classroomID *int
	createdAt   time.Time
	updatedAt   time.Time
	deletedAt   *time.Time
}

// NewTeacher создает новый экземпляр Teacher
func NewTeacher(clock clock.Clock, firstName, lastName string, middleName *string, classroomID *int) (*Teacher, error) {
	now := clock.Now()
	teacher := &Teacher{
		firstName:   firstName,
		lastName:    lastName,
		middleName:  middleName,
		classroomID: classroomID,
		createdAt:   now,
		updatedAt:   now,
	}
	if err := teacher.Validate(); err != nil {
		return nil, err
	}
	return teacher, nil
}

// RestoreTeacherFromDB восстанавливает Teacher из данных БД
func RestoreTeacherFromDB(id int, firstName, lastName string, middleName *string, classroomID *int, createdAt, updatedAt time.Time, deletedAt *time.Time) *Teacher {
	return &Teacher{
		id:          id,
		firstName:   firstName,
		lastName:    lastName,
		middleName:  middleName,
		classroomID: classroomID,
		createdAt:   createdAt,
		updatedAt:   updatedAt,
		deletedAt:   deletedAt,
	}
}

// ID возвращает идентификатор учителя
func (t *Teacher) ID() int {
	return t.id
}

// SetID устанавливает идентификатор (используется только при создании в БД)
func (t *Teacher) SetID(id int) {
	t.id = id
}

// FirstName возвращает имя учителя
func (t *Teacher) FirstName() string {
	return t.firstName
}

// SetFirstName устанавливает имя учителя
func (t *Teacher) SetFirstName(clock clock.Clock, firstName string) {
	t.firstName = firstName
	t.updatedAt = clock.Now()
}

// LastName возвращает фамилию учителя
func (t *Teacher) LastName() string {
	return t.lastName
}

// SetLastName устанавливает фамилию учителя
func (t *Teacher) SetLastName(clock clock.Clock, lastName string) {
	t.lastName = lastName
	t.updatedAt = clock.Now()
}

// MiddleName возвращает отчество учителя
func (t *Teacher) MiddleName() *string {
	return t.middleName
}

// SetMiddleName устанавливает отчество учителя
func (t *Teacher) SetMiddleName(clock clock.Clock, middleName *string) {
	t.middleName = middleName
	t.updatedAt = clock.Now()
}

// ClassroomID возвращает идентификатор кабинета
func (t *Teacher) ClassroomID() *int {
	return t.classroomID
}

// SetClassroomID устанавливает идентификатор кабинета
func (t *Teacher) SetClassroomID(clock clock.Clock, classroomID *int) {
	t.classroomID = classroomID
	t.updatedAt = clock.Now()
}

// CreatedAt возвращает время создания
func (t *Teacher) CreatedAt() time.Time {
	return t.createdAt
}

// UpdatedAt возвращает время обновления
func (t *Teacher) UpdatedAt() time.Time {
	return t.updatedAt
}

// DeletedAt возвращает время удаления
func (t *Teacher) DeletedAt() *time.Time {
	return t.deletedAt
}

// IsDeleted проверяет, удален ли учитель (soft delete)
func (t *Teacher) IsDeleted() bool {
	return t.deletedAt != nil
}

// MarkAsDeleted помечает учителя как удаленного
func (t *Teacher) MarkAsDeleted(clock clock.Clock) {
	now := clock.Now()
	t.deletedAt = &now
	t.updatedAt = now
}

const (
	maxTeacherNameLength = 50
)

// Validate проверяет валидность данных учителя
func (t *Teacher) Validate() error {
	if t.firstName == "" {
		return NewValidationError(entityTeacher, "firstName", t.firstName, "cannot be empty")
	}
	if len(t.firstName) > maxTeacherNameLength {
		return NewValidationError(entityTeacher, "firstName", t.firstName, fmt.Sprintf("length must be <= %d", maxTeacherNameLength))
	}
	if t.lastName == "" {
		return NewValidationError(entityTeacher, "lastName", t.lastName, "cannot be empty")
	}
	if len(t.lastName) > maxTeacherNameLength {
		return NewValidationError(entityTeacher, "lastName", t.lastName, fmt.Sprintf("length must be <= %d", maxTeacherNameLength))
	}
	if t.middleName != nil && len(*t.middleName) > maxTeacherNameLength {
		return NewValidationError(entityTeacher, "middleName", *t.middleName, fmt.Sprintf("length must be <= %d", maxTeacherNameLength))
	}
	return nil
}
