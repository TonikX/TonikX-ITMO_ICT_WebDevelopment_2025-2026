package repository

import (
	"context"
	"database/sql"
	"fmt"
	"time"

	"github.com/Masterminds/squirrel"
	"school-service/internal/domain"
	"school-service/internal/domain/clock"
	"school-service/internal/domain/repository"
)

var _ repository.ScheduleRepository = (*ScheduleRepository)(nil)

// ScheduleRepository реализация репозитория расписания
type ScheduleRepository struct {
	db      *sql.DB
	builder squirrel.StatementBuilderType
	clock   clock.Clock
}

// NewScheduleRepository создает новый репозиторий расписания
func NewScheduleRepository(db *sql.DB, clock clock.Clock) *ScheduleRepository {
	return &ScheduleRepository{
		db:      db,
		builder: squirrel.StatementBuilder.PlaceholderFormat(squirrel.Dollar),
		clock:   clock,
	}
}

// Create создает новую запись расписания
func (r *ScheduleRepository) Create(ctx context.Context, schedule *domain.Schedule) error {
	query := r.builder.
		Insert("schedule").
		Columns("class_id", "weekday_id", "lesson_number", "subject_id", "teacher_id", "classroom_id", "created_at", "updated_at").
		Values(
			schedule.ClassID(),
			schedule.WeekdayID(),
			schedule.LessonNumber(),
			schedule.SubjectID(),
			schedule.TeacherID(),
			schedule.ClassroomID(),
			schedule.CreatedAt(),
			schedule.UpdatedAt(),
		).
		Suffix("RETURNING id")

	var id int
	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(&id)
	if err != nil {
		return fmt.Errorf("failed to create schedule: %w", err)
	}

	schedule.SetID(id)

	return nil
}

// GetByID возвращает запись расписания по ID
func (r *ScheduleRepository) GetByID(ctx context.Context, id int) (*domain.Schedule, error) {
	query := r.builder.
		Select("id", "class_id", "weekday_id", "lesson_number", "subject_id", "teacher_id", "classroom_id", "created_at", "updated_at").
		From("schedule").
		Where(squirrel.Eq{"id": id})

	var (
		scheduleID   int
		classID      int
		weekdayID    int
		lessonNumber int
		subjectID    int
		teacherID    int
		classroomID  int
		createdAt    time.Time
		updatedAt    time.Time
	)

	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(
		&scheduleID,
		&classID,
		&weekdayID,
		&lessonNumber,
		&subjectID,
		&teacherID,
		&classroomID,
		&createdAt,
		&updatedAt,
	)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, domain.NewNotFoundError("Schedule", "id", id, fmt.Sprintf("schedule with id %d not found", id))
		}
		return nil, fmt.Errorf("failed to get schedule by id: %w", err)
	}

	return domain.RestoreScheduleFromDB(
		scheduleID,
		classID,
		weekdayID,
		lessonNumber,
		subjectID,
		teacherID,
		classroomID,
		createdAt,
		updatedAt,
	), nil
}

// Update обновляет запись расписания
func (r *ScheduleRepository) Update(ctx context.Context, schedule *domain.Schedule) error {
	query := r.builder.
		Update("schedule").
		Set("class_id", schedule.ClassID()).
		Set("weekday_id", schedule.WeekdayID()).
		Set("lesson_number", schedule.LessonNumber()).
		Set("subject_id", schedule.SubjectID()).
		Set("teacher_id", schedule.TeacherID()).
		Set("classroom_id", schedule.ClassroomID()).
		Set("updated_at", schedule.UpdatedAt()).
		Where(squirrel.Eq{"id": schedule.ID()})

	result, err := query.RunWith(r.db).ExecContext(ctx)
	if err != nil {
		return fmt.Errorf("failed to update schedule: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get rows affected: %w", err)
	}

	if rowsAffected == 0 {
		return domain.NewNotFoundError("Schedule", "id", schedule.ID(), fmt.Sprintf("schedule with id %d not found", schedule.ID()))
	}

	return nil
}

// Delete удаляет запись расписания
func (r *ScheduleRepository) Delete(ctx context.Context, id int) error {
	query := r.builder.
		Delete("schedule").
		Where(squirrel.Eq{"id": id})

	result, err := query.RunWith(r.db).ExecContext(ctx)
	if err != nil {
		return fmt.Errorf("failed to delete schedule: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get rows affected: %w", err)
	}

	if rowsAffected == 0 {
		return domain.NewNotFoundError("Schedule", "id", id, fmt.Sprintf("schedule with id %d not found", id))
	}

	return nil
}

// List возвращает список всех записей расписания
func (r *ScheduleRepository) List(ctx context.Context) ([]*domain.Schedule, error) {
	query := r.builder.
		Select("id", "class_id", "weekday_id", "lesson_number", "subject_id", "teacher_id", "classroom_id", "created_at", "updated_at").
		From("schedule").
		OrderBy("class_id", "weekday_id", "lesson_number")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list schedules: %w", err)
	}
	defer rows.Close()

	var schedules []*domain.Schedule
	for rows.Next() {
		var (
			scheduleID   int
			classID      int
			weekdayID    int
			lessonNumber int
			subjectID    int
			teacherID    int
			classroomID  int
			createdAt    time.Time
			updatedAt    time.Time
		)

		if err := rows.Scan(
			&scheduleID,
			&classID,
			&weekdayID,
			&lessonNumber,
			&subjectID,
			&teacherID,
			&classroomID,
			&createdAt,
			&updatedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan schedule: %w", err)
		}

		schedule := domain.RestoreScheduleFromDB(
			scheduleID,
			classID,
			weekdayID,
			lessonNumber,
			subjectID,
			teacherID,
			classroomID,
			createdAt,
			updatedAt,
		)
		schedules = append(schedules, schedule)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate schedules: %w", err)
	}

	return schedules, nil
}

// ListByClassID возвращает расписание для класса
func (r *ScheduleRepository) ListByClassID(ctx context.Context, classID int) ([]*domain.Schedule, error) {
	query := r.builder.
		Select("id", "class_id", "weekday_id", "lesson_number", "subject_id", "teacher_id", "classroom_id", "created_at", "updated_at").
		From("schedule").
		Where(squirrel.Eq{"class_id": classID}).
		OrderBy("weekday_id", "lesson_number")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list schedules by class: %w", err)
	}
	defer rows.Close()

	var schedules []*domain.Schedule
	for rows.Next() {
		var (
			scheduleID   int
			classIDVal   int
			weekdayID    int
			lessonNumber int
			subjectID    int
			teacherID    int
			classroomID  int
			createdAt    time.Time
			updatedAt    time.Time
		)

		if err := rows.Scan(
			&scheduleID,
			&classIDVal,
			&weekdayID,
			&lessonNumber,
			&subjectID,
			&teacherID,
			&classroomID,
			&createdAt,
			&updatedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan schedule: %w", err)
		}

		schedule := domain.RestoreScheduleFromDB(
			scheduleID,
			classIDVal,
			weekdayID,
			lessonNumber,
			subjectID,
			teacherID,
			classroomID,
			createdAt,
			updatedAt,
		)
		schedules = append(schedules, schedule)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate schedules: %w", err)
	}

	return schedules, nil
}

// GetByClassAndWeekdayAndLesson возвращает предмет в заданном классе, день недели и номер урока
func (r *ScheduleRepository) GetByClassAndWeekdayAndLesson(ctx context.Context, classID, weekdayID, lessonNumber int) (*domain.Schedule, error) {
	query := r.builder.
		Select("id", "class_id", "weekday_id", "lesson_number", "subject_id", "teacher_id", "classroom_id", "created_at", "updated_at").
		From("schedule").
		Where(squirrel.Eq{
			"class_id":      classID,
			"weekday_id":    weekdayID,
			"lesson_number": lessonNumber,
		})

	var (
		scheduleID      int
		classIDVal      int
		weekdayIDVal    int
		lessonNumberVal int
		subjectID       int
		teacherID       int
		classroomID     int
		createdAt       time.Time
		updatedAt       time.Time
	)

	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(
		&scheduleID,
		&classIDVal,
		&weekdayIDVal,
		&lessonNumberVal,
		&subjectID,
		&teacherID,
		&classroomID,
		&createdAt,
		&updatedAt,
	)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, domain.NewNotFoundError("Schedule", "class_id,weekday_id,lesson_number", fmt.Sprintf("%d,%d,%d", classID, weekdayID, lessonNumber), fmt.Sprintf("schedule not found for class %d, weekday %d, lesson %d", classID, weekdayID, lessonNumber))
		}
		return nil, fmt.Errorf("failed to get schedule: %w", err)
	}

	return domain.RestoreScheduleFromDB(
		scheduleID,
		classIDVal,
		weekdayIDVal,
		lessonNumberVal,
		subjectID,
		teacherID,
		classroomID,
		createdAt,
		updatedAt,
	), nil
}
