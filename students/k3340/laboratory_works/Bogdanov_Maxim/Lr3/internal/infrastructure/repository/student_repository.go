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

var _ repository.StudentRepository = (*StudentRepository)(nil)

// StudentRepository реализация репозитория учеников
type StudentRepository struct {
	db      *sql.DB
	builder squirrel.StatementBuilderType
	clock   clock.Clock
}

// NewStudentRepository создает новый репозиторий учеников
func NewStudentRepository(db *sql.DB, clock clock.Clock) *StudentRepository {
	return &StudentRepository{
		db:      db,
		builder: squirrel.StatementBuilder.PlaceholderFormat(squirrel.Dollar),
		clock:   clock,
	}
}

// Create создает нового ученика
func (r *StudentRepository) Create(ctx context.Context, student *domain.Student) error {
	query := r.builder.
		Insert("students").
		Columns("first_name", "last_name", "middle_name", "gender_id", "class_id", "created_at", "updated_at").
		Values(
			student.FirstName(),
			student.LastName(),
			student.MiddleName(),
			student.GenderID(),
			student.ClassID(),
			student.CreatedAt(),
			student.UpdatedAt(),
		).
		Suffix("RETURNING id")

	var id int
	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(&id)
	if err != nil {
		return fmt.Errorf("failed to create student: %w", err)
	}

	student.SetID(id)

	return nil
}

// GetByID возвращает ученика по ID (включая удаленных)
func (r *StudentRepository) GetByID(ctx context.Context, id int) (*domain.Student, error) {
	query := r.builder.
		Select("id", "first_name", "last_name", "middle_name", "gender_id", "class_id", "created_at", "updated_at", "deleted_at").
		From("students").
		Where(squirrel.Eq{"id": id})

	var (
		studentID  int
		firstName  string
		lastName   string
		middleName sql.NullString
		genderID   int
		classID    int
		createdAt  time.Time
		updatedAt  time.Time
		deletedAt  sql.NullTime
	)

	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(
		&studentID,
		&firstName,
		&lastName,
		&middleName,
		&genderID,
		&classID,
		&createdAt,
		&updatedAt,
		&deletedAt,
	)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, domain.NewNotFoundError("Student", "id", id, fmt.Sprintf("student with id %d not found", id))
		}
		return nil, fmt.Errorf("failed to get student by id: %w", err)
	}

	var middleNamePtr *string
	if middleName.Valid {
		middleNamePtr = &middleName.String
	}

	var deletedAtPtr *time.Time
	if deletedAt.Valid {
		deletedAtPtr = &deletedAt.Time
	}

	return domain.RestoreStudentFromDB(
		studentID,
		firstName,
		lastName,
		middleNamePtr,
		genderID,
		classID,
		createdAt,
		updatedAt,
		deletedAtPtr,
	), nil
}

// GetByIDActive возвращает активного (не удаленного) ученика по ID
func (r *StudentRepository) GetByIDActive(ctx context.Context, id int) (*domain.Student, error) {
	query := r.builder.
		Select("id", "first_name", "last_name", "middle_name", "gender_id", "class_id", "created_at", "updated_at", "deleted_at").
		From("students").
		Where(squirrel.Eq{"id": id}).
		Where(squirrel.Expr("deleted_at IS NULL"))

	var (
		studentID  int
		firstName  string
		lastName   string
		middleName sql.NullString
		genderID   int
		classID    int
		createdAt  time.Time
		updatedAt  time.Time
		deletedAt  sql.NullTime
	)

	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(
		&studentID,
		&firstName,
		&lastName,
		&middleName,
		&genderID,
		&classID,
		&createdAt,
		&updatedAt,
		&deletedAt,
	)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, domain.NewNotFoundError("Student", "id", id, fmt.Sprintf("active student with id %d not found", id))
		}
		return nil, fmt.Errorf("failed to get active student by id: %w", err)
	}

	var middleNamePtr *string
	if middleName.Valid {
		middleNamePtr = &middleName.String
	}

	return domain.RestoreStudentFromDB(
		studentID,
		firstName,
		lastName,
		middleNamePtr,
		genderID,
		classID,
		createdAt,
		updatedAt,
		nil, // deleted_at всегда nil для активных
	), nil
}

// Update обновляет данные ученика
func (r *StudentRepository) Update(ctx context.Context, student *domain.Student) error {
	query := r.builder.
		Update("students").
		Set("first_name", student.FirstName()).
		Set("last_name", student.LastName()).
		Set("middle_name", student.MiddleName()).
		Set("gender_id", student.GenderID()).
		Set("class_id", student.ClassID()).
		Set("updated_at", student.UpdatedAt()).
		Where(squirrel.Eq{"id": student.ID()})

	result, err := query.RunWith(r.db).ExecContext(ctx)
	if err != nil {
		return fmt.Errorf("failed to update student: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get rows affected: %w", err)
	}

	if rowsAffected == 0 {
		return domain.NewNotFoundError("Student", "id", student.ID(), fmt.Sprintf("student with id %d not found", student.ID()))
	}

	return nil
}

// Delete выполняет soft delete ученика
func (r *StudentRepository) Delete(ctx context.Context, id int) error {
	now := r.clock.Now()
	query := r.builder.
		Update("students").
		Set("deleted_at", now).
		Set("updated_at", now).
		Where(squirrel.Eq{"id": id}).
		Where(squirrel.Expr("deleted_at IS NULL"))

	result, err := query.RunWith(r.db).ExecContext(ctx)
	if err != nil {
		return fmt.Errorf("failed to delete student: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get rows affected: %w", err)
	}

	if rowsAffected == 0 {
		return domain.NewNotFoundError("Student", "id", id, fmt.Sprintf("active student with id %d not found", id))
	}

	return nil
}

// List возвращает список всех учеников (включая удаленных)
func (r *StudentRepository) List(ctx context.Context) ([]*domain.Student, error) {
	query := r.builder.
		Select("id", "first_name", "last_name", "middle_name", "gender_id", "class_id", "created_at", "updated_at", "deleted_at").
		From("students").
		OrderBy("id")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list students: %w", err)
	}
	defer rows.Close()

	var students []*domain.Student
	for rows.Next() {
		var (
			studentID  int
			firstName  string
			lastName   string
			middleName sql.NullString
			genderID   int
			classID    int
			createdAt  time.Time
			updatedAt  time.Time
			deletedAt  sql.NullTime
		)

		if err := rows.Scan(
			&studentID,
			&firstName,
			&lastName,
			&middleName,
			&genderID,
			&classID,
			&createdAt,
			&updatedAt,
			&deletedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan student: %w", err)
		}

		var middleNamePtr *string
		if middleName.Valid {
			middleNamePtr = &middleName.String
		}

		var deletedAtPtr *time.Time
		if deletedAt.Valid {
			deletedAtPtr = &deletedAt.Time
		}

		student := domain.RestoreStudentFromDB(
			studentID,
			firstName,
			lastName,
			middleNamePtr,
			genderID,
			classID,
			createdAt,
			updatedAt,
			deletedAtPtr,
		)
		students = append(students, student)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate students: %w", err)
	}

	return students, nil
}

// ListActive возвращает список активных (не удаленных) учеников
func (r *StudentRepository) ListActive(ctx context.Context) ([]*domain.Student, error) {
	query := r.builder.
		Select("id", "first_name", "last_name", "middle_name", "gender_id", "class_id", "created_at", "updated_at", "deleted_at").
		From("students").
		Where(squirrel.Expr("deleted_at IS NULL")).
		OrderBy("id")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list active students: %w", err)
	}
	defer rows.Close()

	var students []*domain.Student
	for rows.Next() {
		var (
			studentID  int
			firstName  string
			lastName   string
			middleName sql.NullString
			genderID   int
			classID    int
			createdAt  time.Time
			updatedAt  time.Time
			deletedAt  sql.NullTime
		)

		if err := rows.Scan(
			&studentID,
			&firstName,
			&lastName,
			&middleName,
			&genderID,
			&classID,
			&createdAt,
			&updatedAt,
			&deletedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan student: %w", err)
		}

		var middleNamePtr *string
		if middleName.Valid {
			middleNamePtr = &middleName.String
		}

		student := domain.RestoreStudentFromDB(
			studentID,
			firstName,
			lastName,
			middleNamePtr,
			genderID,
			classID,
			createdAt,
			updatedAt,
			nil, // deleted_at всегда nil для активных
		)
		students = append(students, student)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate active students: %w", err)
	}

	return students, nil
}

// ListByClassID возвращает список учеников класса
func (r *StudentRepository) ListByClassID(ctx context.Context, classID int) ([]*domain.Student, error) {
	query := r.builder.
		Select("id", "first_name", "last_name", "middle_name", "gender_id", "class_id", "created_at", "updated_at", "deleted_at").
		From("students").
		Where(squirrel.Eq{"class_id": classID}).
		OrderBy("id")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list students by class id: %w", err)
	}
	defer rows.Close()

	var students []*domain.Student
	for rows.Next() {
		var (
			studentID  int
			firstName  string
			lastName   string
			middleName sql.NullString
			genderID   int
			classIDVal int
			createdAt  time.Time
			updatedAt  time.Time
			deletedAt  sql.NullTime
		)

		if err := rows.Scan(
			&studentID,
			&firstName,
			&lastName,
			&middleName,
			&genderID,
			&classIDVal,
			&createdAt,
			&updatedAt,
			&deletedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan student: %w", err)
		}

		var middleNamePtr *string
		if middleName.Valid {
			middleNamePtr = &middleName.String
		}

		var deletedAtPtr *time.Time
		if deletedAt.Valid {
			deletedAtPtr = &deletedAt.Time
		}

		student := domain.RestoreStudentFromDB(
			studentID,
			firstName,
			lastName,
			middleNamePtr,
			genderID,
			classIDVal,
			createdAt,
			updatedAt,
			deletedAtPtr,
		)
		students = append(students, student)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate students by class id: %w", err)
	}

	return students, nil
}

// ListActiveByClassID возвращает список активных учеников класса
func (r *StudentRepository) ListActiveByClassID(ctx context.Context, classID int) ([]*domain.Student, error) {
	query := r.builder.
		Select("id", "first_name", "last_name", "middle_name", "gender_id", "class_id", "created_at", "updated_at", "deleted_at").
		From("students").
		Where(squirrel.Eq{"class_id": classID}).
		Where(squirrel.Expr("deleted_at IS NULL")).
		OrderBy("id")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list active students by class id: %w", err)
	}
	defer rows.Close()

	var students []*domain.Student
	for rows.Next() {
		var (
			studentID  int
			firstName  string
			lastName   string
			middleName sql.NullString
			genderID   int
			classIDVal int
			createdAt  time.Time
			updatedAt  time.Time
			deletedAt  sql.NullTime
		)

		if err := rows.Scan(
			&studentID,
			&firstName,
			&lastName,
			&middleName,
			&genderID,
			&classIDVal,
			&createdAt,
			&updatedAt,
			&deletedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan student: %w", err)
		}

		var middleNamePtr *string
		if middleName.Valid {
			middleNamePtr = &middleName.String
		}

		student := domain.RestoreStudentFromDB(
			studentID,
			firstName,
			lastName,
			middleNamePtr,
			genderID,
			classIDVal,
			createdAt,
			updatedAt,
			nil, // deleted_at всегда nil для активных
		)
		students = append(students, student)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate active students by class id: %w", err)
	}

	return students, nil
}
