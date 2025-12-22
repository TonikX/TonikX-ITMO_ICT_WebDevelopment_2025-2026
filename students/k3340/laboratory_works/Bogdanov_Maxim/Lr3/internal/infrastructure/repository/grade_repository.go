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

var _ repository.GradeRepository = (*GradeRepository)(nil)

// GradeRepository реализация репозитория оценок
type GradeRepository struct {
	db      *sql.DB
	builder squirrel.StatementBuilderType
	clock   clock.Clock
}

// NewGradeRepository создает новый репозиторий оценок
func NewGradeRepository(db *sql.DB, clock clock.Clock) *GradeRepository {
	return &GradeRepository{
		db:      db,
		builder: squirrel.StatementBuilder.PlaceholderFormat(squirrel.Dollar),
		clock:   clock,
	}
}

// Create создает новую оценку
func (r *GradeRepository) Create(ctx context.Context, grade *domain.Grade) error {
	query := r.builder.
		Insert("grades").
		Columns("student_id", "subject_id", "grading_period_id", "grade", "created_at", "updated_at").
		Values(
			grade.StudentID(),
			grade.SubjectID(),
			grade.GradingPeriodID(),
			grade.Grade(),
			grade.CreatedAt(),
			grade.UpdatedAt(),
		).
		Suffix("RETURNING id")

	var id int
	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(&id)
	if err != nil {
		return fmt.Errorf("failed to create grade: %w", err)
	}

	grade.SetID(id)

	return nil
}

// GetByID возвращает оценку по ID
func (r *GradeRepository) GetByID(ctx context.Context, id int) (*domain.Grade, error) {
	query := r.builder.
		Select("id", "student_id", "subject_id", "grading_period_id", "grade", "created_at", "updated_at").
		From("grades").
		Where(squirrel.Eq{"id": id})

	var (
		gradeID         int
		studentID       int
		subjectID       int
		gradingPeriodID int
		grade           int
		createdAt       time.Time
		updatedAt       time.Time
	)

	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(
		&gradeID,
		&studentID,
		&subjectID,
		&gradingPeriodID,
		&grade,
		&createdAt,
		&updatedAt,
	)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, domain.NewNotFoundError("Grade", "id", id, fmt.Sprintf("grade with id %d not found", id))
		}
		return nil, fmt.Errorf("failed to get grade by id: %w", err)
	}

	return domain.RestoreGradeFromDB(
		gradeID,
		studentID,
		subjectID,
		gradingPeriodID,
		grade,
		createdAt,
		updatedAt,
	), nil
}

// Update обновляет оценку
func (r *GradeRepository) Update(ctx context.Context, grade *domain.Grade) error {
	query := r.builder.
		Update("grades").
		Set("student_id", grade.StudentID()).
		Set("subject_id", grade.SubjectID()).
		Set("grading_period_id", grade.GradingPeriodID()).
		Set("grade", grade.Grade()).
		Set("updated_at", grade.UpdatedAt()).
		Where(squirrel.Eq{"id": grade.ID()})

	result, err := query.RunWith(r.db).ExecContext(ctx)
	if err != nil {
		return fmt.Errorf("failed to update grade: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get rows affected: %w", err)
	}

	if rowsAffected == 0 {
		return domain.NewNotFoundError("Grade", "id", grade.ID(), fmt.Sprintf("grade with id %d not found", grade.ID()))
	}

	return nil
}

// Delete удаляет оценку
func (r *GradeRepository) Delete(ctx context.Context, id int) error {
	query := r.builder.
		Delete("grades").
		Where(squirrel.Eq{"id": id})

	result, err := query.RunWith(r.db).ExecContext(ctx)
	if err != nil {
		return fmt.Errorf("failed to delete grade: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get rows affected: %w", err)
	}

	if rowsAffected == 0 {
		return domain.NewNotFoundError("Grade", "id", id, fmt.Sprintf("grade with id %d not found", id))
	}

	return nil
}

// List возвращает список всех оценок
func (r *GradeRepository) List(ctx context.Context) ([]*domain.Grade, error) {
	query := r.builder.
		Select("id", "student_id", "subject_id", "grading_period_id", "grade", "created_at", "updated_at").
		From("grades").
		OrderBy("student_id", "subject_id", "grading_period_id")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list grades: %w", err)
	}
	defer rows.Close()

	var grades []*domain.Grade
	for rows.Next() {
		var (
			gradeID         int
			studentID       int
			subjectID       int
			gradingPeriodID int
			grade           int
			createdAt       time.Time
			updatedAt       time.Time
		)

		if err := rows.Scan(
			&gradeID,
			&studentID,
			&subjectID,
			&gradingPeriodID,
			&grade,
			&createdAt,
			&updatedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan grade: %w", err)
		}

		gradeEntity := domain.RestoreGradeFromDB(
			gradeID,
			studentID,
			subjectID,
			gradingPeriodID,
			grade,
			createdAt,
			updatedAt,
		)
		grades = append(grades, gradeEntity)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate grades: %w", err)
	}

	return grades, nil
}

// ListByStudentID возвращает оценки ученика
func (r *GradeRepository) ListByStudentID(ctx context.Context, studentID int) ([]*domain.Grade, error) {
	query := r.builder.
		Select("id", "student_id", "subject_id", "grading_period_id", "grade", "created_at", "updated_at").
		From("grades").
		Where(squirrel.Eq{"student_id": studentID}).
		OrderBy("subject_id", "grading_period_id")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list grades by student: %w", err)
	}
	defer rows.Close()

	var grades []*domain.Grade
	for rows.Next() {
		var (
			gradeID         int
			studentIDVal    int
			subjectID       int
			gradingPeriodID int
			grade           int
			createdAt       time.Time
			updatedAt       time.Time
		)

		if err := rows.Scan(
			&gradeID,
			&studentIDVal,
			&subjectID,
			&gradingPeriodID,
			&grade,
			&createdAt,
			&updatedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan grade: %w", err)
		}

		gradeEntity := domain.RestoreGradeFromDB(
			gradeID,
			studentIDVal,
			subjectID,
			gradingPeriodID,
			grade,
			createdAt,
			updatedAt,
		)
		grades = append(grades, gradeEntity)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate grades: %w", err)
	}

	return grades, nil
}

// ListByClassID возвращает оценки всех учеников класса
func (r *GradeRepository) ListByClassID(ctx context.Context, classID int) ([]*domain.Grade, error) {
	query := r.builder.
		Select("g.id", "g.student_id", "g.subject_id", "g.grading_period_id", "g.grade", "g.created_at", "g.updated_at").
		From("grades g").
		Join("students s ON g.student_id = s.id").
		Where(squirrel.Eq{"s.class_id": classID}).
		Where(squirrel.Expr("s.deleted_at IS NULL")).
		OrderBy("g.student_id", "g.subject_id", "g.grading_period_id")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list grades by class: %w", err)
	}
	defer rows.Close()

	var grades []*domain.Grade
	for rows.Next() {
		var (
			gradeID         int
			studentID       int
			subjectID       int
			gradingPeriodID int
			grade           int
			createdAt       time.Time
			updatedAt       time.Time
		)

		if err := rows.Scan(
			&gradeID,
			&studentID,
			&subjectID,
			&gradingPeriodID,
			&grade,
			&createdAt,
			&updatedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan grade: %w", err)
		}

		gradeEntity := domain.RestoreGradeFromDB(
			gradeID,
			studentID,
			subjectID,
			gradingPeriodID,
			grade,
			createdAt,
			updatedAt,
		)
		grades = append(grades, gradeEntity)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate grades: %w", err)
	}

	return grades, nil
}

// ListBySubjectID возвращает оценки по предмету
func (r *GradeRepository) ListBySubjectID(ctx context.Context, subjectID int) ([]*domain.Grade, error) {
	query := r.builder.
		Select("id", "student_id", "subject_id", "grading_period_id", "grade", "created_at", "updated_at").
		From("grades").
		Where(squirrel.Eq{"subject_id": subjectID}).
		OrderBy("student_id", "grading_period_id")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list grades by subject: %w", err)
	}
	defer rows.Close()

	var grades []*domain.Grade
	for rows.Next() {
		var (
			gradeID         int
			studentID       int
			subjectIDVal    int
			gradingPeriodID int
			grade           int
			createdAt       time.Time
			updatedAt       time.Time
		)

		if err := rows.Scan(
			&gradeID,
			&studentID,
			&subjectIDVal,
			&gradingPeriodID,
			&grade,
			&createdAt,
			&updatedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan grade: %w", err)
		}

		gradeEntity := domain.RestoreGradeFromDB(
			gradeID,
			studentID,
			subjectIDVal,
			gradingPeriodID,
			grade,
			createdAt,
			updatedAt,
		)
		grades = append(grades, gradeEntity)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate grades: %w", err)
	}

	return grades, nil
}

// ListByClassAndSubject возвращает оценки класса по предмету
func (r *GradeRepository) ListByClassAndSubject(ctx context.Context, classID, subjectID int) ([]*domain.Grade, error) {
	query := r.builder.
		Select("g.id", "g.student_id", "g.subject_id", "g.grading_period_id", "g.grade", "g.created_at", "g.updated_at").
		From("grades g").
		Join("students s ON g.student_id = s.id").
		Where(squirrel.Eq{"s.class_id": classID, "g.subject_id": subjectID}).
		Where(squirrel.Expr("s.deleted_at IS NULL")).
		OrderBy("g.student_id", "g.grading_period_id")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list grades by class and subject: %w", err)
	}
	defer rows.Close()

	var grades []*domain.Grade
	for rows.Next() {
		var (
			gradeID         int
			studentID       int
			subjectIDVal    int
			gradingPeriodID int
			grade           int
			createdAt       time.Time
			updatedAt       time.Time
		)

		if err := rows.Scan(
			&gradeID,
			&studentID,
			&subjectIDVal,
			&gradingPeriodID,
			&grade,
			&createdAt,
			&updatedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan grade: %w", err)
		}

		gradeEntity := domain.RestoreGradeFromDB(
			gradeID,
			studentID,
			subjectIDVal,
			gradingPeriodID,
			grade,
			createdAt,
			updatedAt,
		)
		grades = append(grades, gradeEntity)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate grades: %w", err)
	}

	return grades, nil
}

// ListByClassAndGradingPeriod возвращает оценки класса за оценочный период
func (r *GradeRepository) ListByClassAndGradingPeriod(ctx context.Context, classID, gradingPeriodID int) ([]*domain.Grade, error) {
	query := r.builder.
		Select("g.id", "g.student_id", "g.subject_id", "g.grading_period_id", "g.grade", "g.created_at", "g.updated_at").
		From("grades g").
		Join("students s ON g.student_id = s.id").
		Where(squirrel.Eq{"s.class_id": classID, "g.grading_period_id": gradingPeriodID}).
		Where(squirrel.Expr("s.deleted_at IS NULL")).
		OrderBy("g.student_id", "g.subject_id")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list grades by class and grading period: %w", err)
	}
	defer rows.Close()

	var grades []*domain.Grade
	for rows.Next() {
		var (
			gradeID            int
			studentID          int
			subjectID          int
			gradingPeriodIDVal int
			grade              int
			createdAt          time.Time
			updatedAt          time.Time
		)

		if err := rows.Scan(
			&gradeID,
			&studentID,
			&subjectID,
			&gradingPeriodIDVal,
			&grade,
			&createdAt,
			&updatedAt,
		); err != nil {
			return nil, fmt.Errorf("failed to scan grade: %w", err)
		}

		gradeEntity := domain.RestoreGradeFromDB(
			gradeID,
			studentID,
			subjectID,
			gradingPeriodIDVal,
			grade,
			createdAt,
			updatedAt,
		)
		grades = append(grades, gradeEntity)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate grades: %w", err)
	}

	return grades, nil
}
