package domain

import (
	"fmt"
	"time"

	"school-service/internal/domain/clock"
)

const (
	entitySchedule = "Schedule"
)

// Schedule представляет запись расписания
type Schedule struct {
	id           int
	classID      int
	weekdayID    int
	lessonNumber int
	subjectID    int
	teacherID    int
	classroomID  int
	createdAt    time.Time
	updatedAt    time.Time
}

// NewSchedule создает новый экземпляр Schedule
func NewSchedule(clock clock.Clock, classID, weekdayID, lessonNumber, subjectID, teacherID, classroomID int) (*Schedule, error) {
	now := clock.Now()
	schedule := &Schedule{
		classID:      classID,
		weekdayID:    weekdayID,
		lessonNumber: lessonNumber,
		subjectID:    subjectID,
		teacherID:    teacherID,
		classroomID:  classroomID,
		createdAt:    now,
		updatedAt:    now,
	}
	if err := schedule.Validate(); err != nil {
		return nil, err
	}
	return schedule, nil
}

// RestoreScheduleFromDB восстанавливает Schedule из данных БД
func RestoreScheduleFromDB(id, classID, weekdayID, lessonNumber, subjectID, teacherID, classroomID int, createdAt, updatedAt time.Time) *Schedule {
	return &Schedule{
		id:           id,
		classID:      classID,
		weekdayID:    weekdayID,
		lessonNumber: lessonNumber,
		subjectID:    subjectID,
		teacherID:    teacherID,
		classroomID:  classroomID,
		createdAt:    createdAt,
		updatedAt:    updatedAt,
	}
}

// ID возвращает идентификатор записи расписания
func (s *Schedule) ID() int {
	return s.id
}

// SetID устанавливает идентификатор (используется только при создании в БД)
func (s *Schedule) SetID(id int) {
	s.id = id
}

// ClassID возвращает идентификатор класса
func (s *Schedule) ClassID() int {
	return s.classID
}

// SetClassID устанавливает идентификатор класса
func (s *Schedule) SetClassID(clock clock.Clock, classID int) {
	s.classID = classID
	s.updatedAt = clock.Now()
}

// WeekdayID возвращает идентификатор дня недели
func (s *Schedule) WeekdayID() int {
	return s.weekdayID
}

// SetWeekdayID устанавливает идентификатор дня недели
func (s *Schedule) SetWeekdayID(clock clock.Clock, weekdayID int) {
	s.weekdayID = weekdayID
	s.updatedAt = clock.Now()
}

// LessonNumber возвращает номер урока
func (s *Schedule) LessonNumber() int {
	return s.lessonNumber
}

// SetLessonNumber устанавливает номер урока
func (s *Schedule) SetLessonNumber(clock clock.Clock, lessonNumber int) {
	s.lessonNumber = lessonNumber
	s.updatedAt = clock.Now()
}

// SubjectID возвращает идентификатор предмета
func (s *Schedule) SubjectID() int {
	return s.subjectID
}

// SetSubjectID устанавливает идентификатор предмета
func (s *Schedule) SetSubjectID(clock clock.Clock, subjectID int) {
	s.subjectID = subjectID
	s.updatedAt = clock.Now()
}

// TeacherID возвращает идентификатор учителя
func (s *Schedule) TeacherID() int {
	return s.teacherID
}

// SetTeacherID устанавливает идентификатор учителя
func (s *Schedule) SetTeacherID(clock clock.Clock, teacherID int) {
	s.teacherID = teacherID
	s.updatedAt = clock.Now()
}

// ClassroomID возвращает идентификатор кабинета
func (s *Schedule) ClassroomID() int {
	return s.classroomID
}

// SetClassroomID устанавливает идентификатор кабинета
func (s *Schedule) SetClassroomID(clock clock.Clock, classroomID int) {
	s.classroomID = classroomID
	s.updatedAt = clock.Now()
}

// CreatedAt возвращает время создания
func (s *Schedule) CreatedAt() time.Time {
	return s.createdAt
}

// UpdatedAt возвращает время обновления
func (s *Schedule) UpdatedAt() time.Time {
	return s.updatedAt
}

const (
	minLessonNumber = 1
	maxLessonNumber = 10
)

// Validate проверяет валидность данных расписания
func (s *Schedule) Validate() error {
	if s.classID <= 0 {
		return NewValidationError(entitySchedule, "classID", s.classID, "must be > 0")
	}
	if s.weekdayID <= 0 {
		return NewValidationError(entitySchedule, "weekdayID", s.weekdayID, "must be > 0")
	}
	if s.lessonNumber < minLessonNumber || s.lessonNumber > maxLessonNumber {
		return NewValidationError(entitySchedule, "lessonNumber", s.lessonNumber, fmt.Sprintf("must be between %d and %d", minLessonNumber, maxLessonNumber))
	}
	if s.subjectID <= 0 {
		return NewValidationError(entitySchedule, "subjectID", s.subjectID, "must be > 0")
	}
	if s.teacherID <= 0 {
		return NewValidationError(entitySchedule, "teacherID", s.teacherID, "must be > 0")
	}
	if s.classroomID <= 0 {
		return NewValidationError(entitySchedule, "classroomID", s.classroomID, "must be > 0")
	}
	return nil
}
