package domain

import (
	"fmt"
	"time"

	"school-service/internal/domain/clock"
)

const (
	entitySubject = "Subject"
)

// Subject представляет сущность предмета
type Subject struct {
	id            int
	name          string
	subjectTypeID int
	createdAt     time.Time
	updatedAt     time.Time
}

// NewSubject создает новый экземпляр Subject
func NewSubject(clock clock.Clock, name string, subjectTypeID int) (*Subject, error) {
	now := clock.Now()
	subject := &Subject{
		name:          name,
		subjectTypeID: subjectTypeID,
		createdAt:     now,
		updatedAt:     now,
	}
	if err := subject.Validate(); err != nil {
		return nil, err
	}
	return subject, nil
}

// RestoreSubjectFromDB восстанавливает Subject из данных БД
func RestoreSubjectFromDB(id int, name string, subjectTypeID int, createdAt, updatedAt time.Time) *Subject {
	return &Subject{
		id:            id,
		name:          name,
		subjectTypeID: subjectTypeID,
		createdAt:     createdAt,
		updatedAt:     updatedAt,
	}
}

// ID возвращает идентификатор предмета
func (s *Subject) ID() int {
	return s.id
}

// SetID устанавливает идентификатор (используется только при создании в БД)
func (s *Subject) SetID(id int) {
	s.id = id
}

// Name возвращает название предмета
func (s *Subject) Name() string {
	return s.name
}

// SetName устанавливает название предмета
func (s *Subject) SetName(clock clock.Clock, name string) {
	s.name = name
	s.updatedAt = clock.Now()
}

// SubjectTypeID возвращает идентификатор типа предмета
func (s *Subject) SubjectTypeID() int {
	return s.subjectTypeID
}

// SetSubjectTypeID устанавливает идентификатор типа предмета
func (s *Subject) SetSubjectTypeID(clock clock.Clock, subjectTypeID int) {
	s.subjectTypeID = subjectTypeID
	s.updatedAt = clock.Now()
}

// CreatedAt возвращает время создания
func (s *Subject) CreatedAt() time.Time {
	return s.createdAt
}

// UpdatedAt возвращает время обновления
func (s *Subject) UpdatedAt() time.Time {
	return s.updatedAt
}

const (
	maxSubjectNameLength = 100
)

// Validate проверяет валидность данных предмета
func (s *Subject) Validate() error {
	if s.name == "" {
		return NewValidationError(entitySubject, "name", s.name, "cannot be empty")
	}
	if len(s.name) > maxSubjectNameLength {
		return NewValidationError(entitySubject, "name", s.name, fmt.Sprintf("length must be <= %d", maxSubjectNameLength))
	}
	if s.subjectTypeID <= 0 {
		return NewValidationError(entitySubject, "subjectTypeID", s.subjectTypeID, "must be > 0")
	}
	return nil
}
