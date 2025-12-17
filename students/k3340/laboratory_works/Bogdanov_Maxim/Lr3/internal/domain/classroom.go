package domain

import (
	"fmt"
	"time"

	"school-service/internal/domain/clock"
)

const (
	entityClassroom     = "Classroom"
	maxRoomNumberLength = 10
)

// Classroom представляет сущность кабинета
type Classroom struct {
	id            int
	roomNumber    string
	subjectTypeID int
	createdAt     time.Time
	updatedAt     time.Time
}

// NewClassroom создает новый экземпляр Classroom
func NewClassroom(clock clock.Clock, roomNumber string, subjectTypeID int) (*Classroom, error) {
	now := clock.Now()
	classroom := &Classroom{
		roomNumber:    roomNumber,
		subjectTypeID: subjectTypeID,
		createdAt:     now,
		updatedAt:     now,
	}
	if err := classroom.Validate(); err != nil {
		return nil, err
	}
	return classroom, nil
}

// RestoreClassroomFromDB восстанавливает Classroom из данных БД
func RestoreClassroomFromDB(id int, roomNumber string, subjectTypeID int, createdAt, updatedAt time.Time) *Classroom {
	return &Classroom{
		id:            id,
		roomNumber:    roomNumber,
		subjectTypeID: subjectTypeID,
		createdAt:     createdAt,
		updatedAt:     updatedAt,
	}
}

// ID возвращает идентификатор кабинета
func (c *Classroom) ID() int {
	return c.id
}

// SetID устанавливает идентификатор (используется только при создании в БД)
func (c *Classroom) SetID(id int) {
	c.id = id
}

// RoomNumber возвращает номер кабинета
func (c *Classroom) RoomNumber() string {
	return c.roomNumber
}

// SetRoomNumber устанавливает номер кабинета
func (c *Classroom) SetRoomNumber(clock clock.Clock, roomNumber string) {
	c.roomNumber = roomNumber
	c.updatedAt = clock.Now()
}

// SubjectTypeID возвращает идентификатор типа предмета
func (c *Classroom) SubjectTypeID() int {
	return c.subjectTypeID
}

// SetSubjectTypeID устанавливает идентификатор типа предмета
func (c *Classroom) SetSubjectTypeID(clock clock.Clock, subjectTypeID int) {
	c.subjectTypeID = subjectTypeID
	c.updatedAt = clock.Now()
}

// CreatedAt возвращает время создания
func (c *Classroom) CreatedAt() time.Time {
	return c.createdAt
}

// UpdatedAt возвращает время обновления
func (c *Classroom) UpdatedAt() time.Time {
	return c.updatedAt
}

// Validate проверяет валидность данных кабинета
func (c *Classroom) Validate() error {
	if c.roomNumber == "" {
		return NewValidationError(entityClassroom, "roomNumber", c.roomNumber, "cannot be empty")
	}
	if len(c.roomNumber) > maxRoomNumberLength {
		return NewValidationError(entityClassroom, "roomNumber", c.roomNumber, fmt.Sprintf("length must be <= %d", maxRoomNumberLength))
	}
	if c.subjectTypeID <= 0 {
		return NewValidationError(entityClassroom, "subjectTypeID", c.subjectTypeID, "must be > 0")
	}
	return nil
}
