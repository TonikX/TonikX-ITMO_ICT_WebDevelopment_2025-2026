package domain

import (
	"fmt"
	"time"

	"school-service/internal/domain/clock"
)

const (
	entityStudent = "Student"
)

// Student представляет сущность ученика
type Student struct {
	id         int
	firstName  string
	lastName   string
	middleName *string
	genderID   int
	classID    int
	createdAt  time.Time
	updatedAt  time.Time
	deletedAt  *time.Time
}

// NewStudent создает новый экземпляр Student
func NewStudent(clock clock.Clock, firstName, lastName string, middleName *string, genderID, classID int) (*Student, error) {
	now := clock.Now()
	student := &Student{
		firstName:  firstName,
		lastName:   lastName,
		middleName: middleName,
		genderID:   genderID,
		classID:    classID,
		createdAt:  now,
		updatedAt:  now,
	}
	if err := student.Validate(); err != nil {
		return nil, err
	}
	return student, nil
}

// RestoreStudentFromDB восстанавливает Student из данных БД
func RestoreStudentFromDB(id int, firstName, lastName string, middleName *string, genderID, classID int, createdAt, updatedAt time.Time, deletedAt *time.Time) *Student {
	return &Student{
		id:         id,
		firstName:  firstName,
		lastName:   lastName,
		middleName: middleName,
		genderID:   genderID,
		classID:    classID,
		createdAt:  createdAt,
		updatedAt:  updatedAt,
		deletedAt:  deletedAt,
	}
}

// ID возвращает идентификатор ученика
func (s *Student) ID() int {
	return s.id
}

// SetID устанавливает идентификатор (используется только при создании в БД)
func (s *Student) SetID(id int) {
	s.id = id
}

// FirstName возвращает имя ученика
func (s *Student) FirstName() string {
	return s.firstName
}

// SetFirstName устанавливает имя ученика
func (s *Student) SetFirstName(clock clock.Clock, firstName string) {
	s.firstName = firstName
	s.updatedAt = clock.Now()
}

// LastName возвращает фамилию ученика
func (s *Student) LastName() string {
	return s.lastName
}

// SetLastName устанавливает фамилию ученика
func (s *Student) SetLastName(clock clock.Clock, lastName string) {
	s.lastName = lastName
	s.updatedAt = clock.Now()
}

// MiddleName возвращает отчество ученика
func (s *Student) MiddleName() *string {
	return s.middleName
}

// SetMiddleName устанавливает отчество ученика
func (s *Student) SetMiddleName(clock clock.Clock, middleName *string) {
	s.middleName = middleName
	s.updatedAt = clock.Now()
}

// GenderID возвращает идентификатор пола
func (s *Student) GenderID() int {
	return s.genderID
}

// SetGenderID устанавливает идентификатор пола
func (s *Student) SetGenderID(clock clock.Clock, genderID int) {
	s.genderID = genderID
	s.updatedAt = clock.Now()
}

// ClassID возвращает идентификатор класса
func (s *Student) ClassID() int {
	return s.classID
}

// SetClassID устанавливает идентификатор класса
func (s *Student) SetClassID(clock clock.Clock, classID int) {
	s.classID = classID
	s.updatedAt = clock.Now()
}

// CreatedAt возвращает время создания
func (s *Student) CreatedAt() time.Time {
	return s.createdAt
}

// UpdatedAt возвращает время обновления
func (s *Student) UpdatedAt() time.Time {
	return s.updatedAt
}

// DeletedAt возвращает время удаления
func (s *Student) DeletedAt() *time.Time {
	return s.deletedAt
}

// IsDeleted проверяет, удален ли ученик (soft delete)
func (s *Student) IsDeleted() bool {
	return s.deletedAt != nil
}

// MarkAsDeleted помечает ученика как удаленного
func (s *Student) MarkAsDeleted(clock clock.Clock) {
	now := clock.Now()
	s.deletedAt = &now
	s.updatedAt = now
}

const (
	maxStudentNameLength = 50
)

// Validate проверяет валидность данных ученика
func (s *Student) Validate() error {
	if s.firstName == "" {
		return NewValidationError(entityStudent, "firstName", s.firstName, "cannot be empty")
	}
	if len(s.firstName) > maxStudentNameLength {
		return NewValidationError(entityStudent, "firstName", s.firstName, fmt.Sprintf("length must be <= %d", maxStudentNameLength))
	}
	if s.lastName == "" {
		return NewValidationError(entityStudent, "lastName", s.lastName, "cannot be empty")
	}
	if len(s.lastName) > maxStudentNameLength {
		return NewValidationError(entityStudent, "lastName", s.lastName, fmt.Sprintf("length must be <= %d", maxStudentNameLength))
	}
	if s.middleName != nil && len(*s.middleName) > maxStudentNameLength {
		return NewValidationError(entityStudent, "middleName", *s.middleName, fmt.Sprintf("length must be <= %d", maxStudentNameLength))
	}
	if s.genderID <= 0 {
		return NewValidationError(entityStudent, "genderID", s.genderID, "must be > 0")
	}
	if s.classID <= 0 {
		return NewValidationError(entityStudent, "classID", s.classID, "must be > 0")
	}
	return nil
}
