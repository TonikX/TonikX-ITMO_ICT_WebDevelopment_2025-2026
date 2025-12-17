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

var _ repository.TeacherRepository = (*TeacherRepository)(nil)

// TeacherRepository реализация репозитория учителей
type TeacherRepository struct {
	db      *sql.DB
	builder squirrel.StatementBuilderType
	clock   clock.Clock
}

// NewTeacherRepository создает новый репозиторий учителей
func NewTeacherRepository(db *sql.DB, clock clock.Clock) *TeacherRepository {
	return &TeacherRepository{
		db:      db,
		builder: squirrel.StatementBuilder.PlaceholderFormat(squirrel.Dollar),
		clock:   clock,
	}
}

// Create создает нового учителя
func (r *TeacherRepository) Create(ctx context.Context, teacher *domain.Teacher) error {
	query := r.builder.
		Insert("teachers").
		Columns("first_name", "last_name", "middle_name", "classroom_id", "created_at", "updated_at").
		Values(
			teacher.FirstName(),
			teacher.LastName(),
			teacher.MiddleName(),
			teacher.ClassroomID(),
			teacher.CreatedAt(),
			teacher.UpdatedAt(),
		).
		Suffix("RETURNING id")

	var id int
	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(&id)
	if err != nil {
		return fmt.Errorf("failed to create teacher: %w", err)
	}

	teacher.SetID(id)

	return nil
}

// GetByID возвращает учителя по ID (включая удаленных)
func (r *TeacherRepository) GetByID(ctx context.Context, id int) (*domain.Teacher, error) {
	query := r.builder.
		Select("id", "first_name", "last_name", "middle_name", "classroom_id", "created_at", "updated_at", "deleted_at").
		From("teachers").
		Where(squirrel.Eq{"id": id})

	var (
		teacherID   int
		firstName   string
		lastName    string
		middleName  sql.NullString
		classroomID sql.NullInt64
		createdAt   time.Time
		updatedAt   time.Time
		deletedAt   sql.NullTime
	)

	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(
		&teacherID,
		&firstName,
		&lastName,
		&middleName,
		&classroomID,
		&createdAt,
		&updatedAt,
		&deletedAt,
	)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, domain.NewNotFoundError("Teacher", "id", id, fmt.Sprintf("teacher with id %d not found", id))
		}
		return nil, fmt.Errorf("failed to get teacher by id: %w", err)
	}

	var middleNamePtr *string
	if middleName.Valid {
		middleNamePtr = &middleName.String
	}

	var classroomIDPtr *int
	if classroomID.Valid {
		id := int(classroomID.Int64)
		classroomIDPtr = &id
	}

	var deletedAtPtr *time.Time
	if deletedAt.Valid {
		deletedAtPtr = &deletedAt.Time
	}

	return domain.RestoreTeacherFromDB(
		teacherID,
		firstName,
		lastName,
		middleNamePtr,
		classroomIDPtr,
		createdAt,
		updatedAt,
		deletedAtPtr,
	), nil
}

// GetByIDActive возвращает активного (не удаленного) учителя по ID
func (r *TeacherRepository) GetByIDActive(ctx context.Context, id int) (*domain.Teacher, error) {
	query := r.builder.
		Select("id", "first_name", "last_name", "middle_name", "classroom_id", "created_at", "updated_at", "deleted_at").
		From("teachers").
		Where(squirrel.Eq{"id": id}).
		Where(squirrel.Expr("deleted_at IS NULL"))

	var (
		teacherID   int
		firstName   string
		lastName    string
		middleName  sql.NullString
		classroomID sql.NullInt64
		createdAt   time.Time
		updatedAt   time.Time
		deletedAt   sql.NullTime
	)

	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(
		&teacherID,
		&firstName,
		&lastName,
		&middleName,
		&classroomID,
		&createdAt,
		&updatedAt,
		&deletedAt,
	)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, domain.NewNotFoundError("Teacher", "id", id, fmt.Sprintf("active teacher with id %d not found", id))
		}
		return nil, fmt.Errorf("failed to get active teacher by id: %w", err)
	}

	var middleNamePtr *string
	if middleName.Valid {
		middleNamePtr = &middleName.String
	}

	var classroomIDPtr *int
	if classroomID.Valid {
		id := int(classroomID.Int64)
		classroomIDPtr = &id
	}

	return domain.RestoreTeacherFromDB(
		teacherID,
		firstName,
		lastName,
		middleNamePtr,
		classroomIDPtr,
		createdAt,
		updatedAt,
		nil, // deleted_at всегда nil для активных
	), nil
}

// Update обновляет данные учителя
func (r *TeacherRepository) Update(ctx context.Context, teacher *domain.Teacher) error {
	query := r.builder.
		Update("teachers").
		Set("first_name", teacher.FirstName()).
		Set("last_name", teacher.LastName()).
		Set("middle_name", teacher.MiddleName()).
		Set("classroom_id", teacher.ClassroomID()).
		Set("updated_at", teacher.UpdatedAt()).
		Where(squirrel.Eq{"id": teacher.ID()})

	result, err := query.RunWith(r.db).ExecContext(ctx)
	if err != nil {
		return fmt.Errorf("failed to update teacher: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get rows affected: %w", err)
	}

	if rowsAffected == 0 {
		return domain.NewNotFoundError("Teacher", "id", teacher.ID(), fmt.Sprintf("teacher with id %d not found", teacher.ID()))
	}

	return nil
}

// Delete выполняет soft delete учителя
func (r *TeacherRepository) Delete(ctx context.Context, id int) error {
	now := r.clock.Now()
	query := r.builder.
		Update("teachers").
		Set("deleted_at", now).
		Set("updated_at", now).
		Where(squirrel.Eq{"id": id}).
		Where(squirrel.Expr("deleted_at IS NULL"))

	result, err := query.RunWith(r.db).ExecContext(ctx)
	if err != nil {
		return fmt.Errorf("failed to delete teacher: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get rows affected: %w", err)
	}

	if rowsAffected == 0 {
		return domain.NewNotFoundError("Teacher", "id", id, fmt.Sprintf("active teacher with id %d not found", id))
	}

	return nil
}

// List возвращает список всех учителей (включая удаленных)
func (r *TeacherRepository) List(ctx context.Context) ([]*domain.Teacher, error) {
	query := r.builder.
		Select("id", "first_name", "last_name", "middle_name", "classroom_id", "created_at", "updated_at", "deleted_at").
		From("teachers").
		OrderBy("id")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list teachers: %w", err)
	}
	defer rows.Close()

	var teachers []*domain.Teacher
	for rows.Next() {
		var (
			teacherID   int
			firstName   string
			lastName    string
			middleName  sql.NullString
			classroomID sql.NullInt64
			createdAt   time.Time
			updatedAt   time.Time
			deletedAt   sql.NullTime
		)

		if err := rows.Scan(
			&teacherID,
			&firstName,
			&lastName,
			&middleName,
			&classroomID,
			&createdAt,
			&updatedAt,
			&deletedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan teacher: %w", err)
		}

		var middleNamePtr *string
		if middleName.Valid {
			middleNamePtr = &middleName.String
		}

		var classroomIDPtr *int
		if classroomID.Valid {
			id := int(classroomID.Int64)
			classroomIDPtr = &id
		}

		var deletedAtPtr *time.Time
		if deletedAt.Valid {
			deletedAtPtr = &deletedAt.Time
		}

		teacher := domain.RestoreTeacherFromDB(
			teacherID,
			firstName,
			lastName,
			middleNamePtr,
			classroomIDPtr,
			createdAt,
			updatedAt,
			deletedAtPtr,
		)
		teachers = append(teachers, teacher)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate teachers: %w", err)
	}

	return teachers, nil
}

// ListActive возвращает список активных (не удаленных) учителей
func (r *TeacherRepository) ListActive(ctx context.Context) ([]*domain.Teacher, error) {
	query := r.builder.
		Select("id", "first_name", "last_name", "middle_name", "classroom_id", "created_at", "updated_at", "deleted_at").
		From("teachers").
		Where(squirrel.Expr("deleted_at IS NULL")).
		OrderBy("id")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list active teachers: %w", err)
	}
	defer rows.Close()

	var teachers []*domain.Teacher
	for rows.Next() {
		var (
			teacherID   int
			firstName   string
			lastName    string
			middleName  sql.NullString
			classroomID sql.NullInt64
			createdAt   time.Time
			updatedAt   time.Time
			deletedAt   sql.NullTime
		)

		if err := rows.Scan(
			&teacherID,
			&firstName,
			&lastName,
			&middleName,
			&classroomID,
			&createdAt,
			&updatedAt,
			&deletedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan teacher: %w", err)
		}

		var middleNamePtr *string
		if middleName.Valid {
			middleNamePtr = &middleName.String
		}

		var classroomIDPtr *int
		if classroomID.Valid {
			id := int(classroomID.Int64)
			classroomIDPtr = &id
		}

		teacher := domain.RestoreTeacherFromDB(
			teacherID,
			firstName,
			lastName,
			middleNamePtr,
			classroomIDPtr,
			createdAt,
			updatedAt,
			nil, // deleted_at всегда nil для активных
		)
		teachers = append(teachers, teacher)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate active teachers: %w", err)
	}

	return teachers, nil
}
