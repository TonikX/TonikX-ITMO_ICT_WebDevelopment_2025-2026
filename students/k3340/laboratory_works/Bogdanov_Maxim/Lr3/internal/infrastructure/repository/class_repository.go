package repository

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"time"

	"github.com/Masterminds/squirrel"
	"school-service/internal/domain"
	"school-service/internal/domain/clock"
	"school-service/internal/domain/repository"
)

var _ repository.ClassRepository = (*ClassRepository)(nil)

// ClassRepository реализация репозитория классов
type ClassRepository struct {
	db      *sql.DB
	builder squirrel.StatementBuilderType
	clock   clock.Clock
}

// NewClassRepository создает новый репозиторий классов
func NewClassRepository(db *sql.DB, clock clock.Clock) *ClassRepository {
	return &ClassRepository{
		db:      db,
		builder: squirrel.StatementBuilder.PlaceholderFormat(squirrel.Dollar),
		clock:   clock,
	}
}

// Create создает новый класс
func (r *ClassRepository) Create(ctx context.Context, class *domain.Class) error {
	query := r.builder.
		Insert("classes").
		Columns("grade", "letter", "academic_year_id", "class_teacher_id", "created_at", "updated_at").
		Values(
			class.Grade(),
			class.Letter(),
			class.AcademicYearID(),
			class.ClassTeacherID(),
			class.CreatedAt(),
			class.UpdatedAt(),
		).
		Suffix("RETURNING id")

	var id int
	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(&id)
	if err != nil {
		return fmt.Errorf("failed to create class: %w", err)
	}

	class.SetID(id)

	return nil
}

// GetByID возвращает класс по ID (включая удаленные)
func (r *ClassRepository) GetByID(ctx context.Context, id int) (*domain.Class, error) {
	query := r.builder.
		Select("id", "grade", "letter", "academic_year_id", "class_teacher_id", "created_at", "updated_at", "deleted_at").
		From("classes").
		Where(squirrel.Eq{"id": id})

	var (
		classID        int
		grade          int
		letter         string
		academicYearID int
		classTeacherID sql.NullInt64
		createdAt      time.Time
		updatedAt      time.Time
		deletedAt      sql.NullTime
	)

	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(
		&classID,
		&grade,
		&letter,
		&academicYearID,
		&classTeacherID,
		&createdAt,
		&updatedAt,
		&deletedAt,
	)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, domain.NewNotFoundError("Class", "id", id, fmt.Sprintf("class with id %d not found", id))
		}
		return nil, fmt.Errorf("failed to get class by id: %w", err)
	}

	var classTeacherIDPtr *int
	if classTeacherID.Valid {
		id := int(classTeacherID.Int64)
		classTeacherIDPtr = &id
	}

	var deletedAtPtr *time.Time
	if deletedAt.Valid {
		deletedAtPtr = &deletedAt.Time
	}

	return domain.RestoreClassFromDB(
		classID,
		grade,
		letter,
		academicYearID,
		classTeacherIDPtr,
		createdAt,
		updatedAt,
		deletedAtPtr,
	), nil
}

// GetByIDActive возвращает активный (не удаленный) класс по ID
func (r *ClassRepository) GetByIDActive(ctx context.Context, id int) (*domain.Class, error) {
	query := r.builder.
		Select("id", "grade", "letter", "academic_year_id", "class_teacher_id", "created_at", "updated_at", "deleted_at").
		From("classes").
		Where(squirrel.Eq{"id": id}).
		Where(squirrel.Expr("deleted_at IS NULL"))

	var (
		classID        int
		grade          int
		letter         string
		academicYearID int
		classTeacherID sql.NullInt64
		createdAt      time.Time
		updatedAt      time.Time
		deletedAt      sql.NullTime
	)

	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(
		&classID,
		&grade,
		&letter,
		&academicYearID,
		&classTeacherID,
		&createdAt,
		&updatedAt,
		&deletedAt,
	)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, domain.NewNotFoundError("Class", "id", id, fmt.Sprintf("active class with id %d not found", id))
		}
		return nil, fmt.Errorf("failed to get active class by id: %w", err)
	}

	var classTeacherIDPtr *int
	if classTeacherID.Valid {
		id := int(classTeacherID.Int64)
		classTeacherIDPtr = &id
	}

	return domain.RestoreClassFromDB(
		classID,
		grade,
		letter,
		academicYearID,
		classTeacherIDPtr,
		createdAt,
		updatedAt,
		nil,
	), nil
}

// Update обновляет данные класса
func (r *ClassRepository) Update(ctx context.Context, class *domain.Class) error {
	query := r.builder.
		Update("classes").
		Set("grade", class.Grade()).
		Set("letter", class.Letter()).
		Set("academic_year_id", class.AcademicYearID()).
		Set("class_teacher_id", class.ClassTeacherID()).
		Set("updated_at", class.UpdatedAt()).
		Where(squirrel.Eq{"id": class.ID()})

	result, err := query.RunWith(r.db).ExecContext(ctx)
	if err != nil {
		return fmt.Errorf("failed to update class: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get rows affected: %w", err)
	}

	if rowsAffected == 0 {
		return domain.NewNotFoundError("Class", "id", class.ID(), fmt.Sprintf("class with id %d not found", class.ID()))
	}

	return nil
}

// Delete выполняет soft delete класса
func (r *ClassRepository) Delete(ctx context.Context, id int) error {
	now := r.clock.Now()
	query := r.builder.
		Update("classes").
		Set("deleted_at", now).
		Set("updated_at", now).
		Where(squirrel.Eq{"id": id}).
		Where(squirrel.Expr("deleted_at IS NULL"))

	result, err := query.RunWith(r.db).ExecContext(ctx)
	if err != nil {
		return fmt.Errorf("failed to delete class: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get rows affected: %w", err)
	}

	if rowsAffected == 0 {
		return domain.NewNotFoundError("Class", "id", id, fmt.Sprintf("active class with id %d not found", id))
	}

	return nil
}

// List возвращает список всех классов (включая удаленные)
func (r *ClassRepository) List(ctx context.Context) ([]*domain.Class, error) {
	query := r.builder.
		Select("id", "grade", "letter", "academic_year_id", "class_teacher_id", "created_at", "updated_at", "deleted_at").
		From("classes").
		OrderBy("id")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list classes: %w", err)
	}
	defer rows.Close()

	var classes []*domain.Class
	for rows.Next() {
		var (
			classID        int
			grade          int
			letter         string
			academicYearID int
			classTeacherID sql.NullInt64
			createdAt      time.Time
			updatedAt      time.Time
			deletedAt      sql.NullTime
		)

		if err := rows.Scan(
			&classID,
			&grade,
			&letter,
			&academicYearID,
			&classTeacherID,
			&createdAt,
			&updatedAt,
			&deletedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan class: %w", err)
		}

		var classTeacherIDPtr *int
		if classTeacherID.Valid {
			id := int(classTeacherID.Int64)
			classTeacherIDPtr = &id
		}

		var deletedAtPtr *time.Time
		if deletedAt.Valid {
			deletedAtPtr = &deletedAt.Time
		}

		class := domain.RestoreClassFromDB(
			classID,
			grade,
			letter,
			academicYearID,
			classTeacherIDPtr,
			createdAt,
			updatedAt,
			deletedAtPtr,
		)
		classes = append(classes, class)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate classes: %w", err)
	}

	return classes, nil
}

// ListActive возвращает список активных (не удаленных) классов
func (r *ClassRepository) ListActive(ctx context.Context) ([]*domain.Class, error) {
	query := r.builder.
		Select("id", "grade", "letter", "academic_year_id", "class_teacher_id", "created_at", "updated_at", "deleted_at").
		From("classes").
		Where(squirrel.Expr("deleted_at IS NULL")).
		OrderBy("id")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list active classes: %w", err)
	}
	defer rows.Close()

	var classes []*domain.Class
	for rows.Next() {
		var (
			classID        int
			grade          int
			letter         string
			academicYearID int
			classTeacherID sql.NullInt64
			createdAt      time.Time
			updatedAt      time.Time
			deletedAt      sql.NullTime
		)

		if err := rows.Scan(
			&classID,
			&grade,
			&letter,
			&academicYearID,
			&classTeacherID,
			&createdAt,
			&updatedAt,
			&deletedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan class: %w", err)
		}

		var classTeacherIDPtr *int
		if classTeacherID.Valid {
			id := int(classTeacherID.Int64)
			classTeacherIDPtr = &id
		}

		class := domain.RestoreClassFromDB(
			classID,
			grade,
			letter,
			academicYearID,
			classTeacherIDPtr,
			createdAt,
			updatedAt,
			nil,
		)
		classes = append(classes, class)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate active classes: %w", err)
	}

	return classes, nil
}

// ListByAcademicYearID возвращает список классов учебного года
func (r *ClassRepository) ListByAcademicYearID(ctx context.Context, academicYearID int) ([]*domain.Class, error) {
	query := r.builder.
		Select("id", "grade", "letter", "academic_year_id", "class_teacher_id", "created_at", "updated_at", "deleted_at").
		From("classes").
		Where(squirrel.Eq{"academic_year_id": academicYearID}).
		OrderBy("id")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list classes by academic year id: %w", err)
	}
	defer rows.Close()

	var classes []*domain.Class
	for rows.Next() {
		var (
			classID           int
			grade             int
			letter            string
			academicYearIDVal int
			classTeacherID    sql.NullInt64
			createdAt         time.Time
			updatedAt         time.Time
			deletedAt         sql.NullTime
		)

		if err := rows.Scan(
			&classID,
			&grade,
			&letter,
			&academicYearIDVal,
			&classTeacherID,
			&createdAt,
			&updatedAt,
			&deletedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan class: %w", err)
		}

		var classTeacherIDPtr *int
		if classTeacherID.Valid {
			id := int(classTeacherID.Int64)
			classTeacherIDPtr = &id
		}

		var deletedAtPtr *time.Time
		if deletedAt.Valid {
			deletedAtPtr = &deletedAt.Time
		}

		class := domain.RestoreClassFromDB(
			classID,
			grade,
			letter,
			academicYearIDVal,
			classTeacherIDPtr,
			createdAt,
			updatedAt,
			deletedAtPtr,
		)
		classes = append(classes, class)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate classes by academic year id: %w", err)
	}

	return classes, nil
}
