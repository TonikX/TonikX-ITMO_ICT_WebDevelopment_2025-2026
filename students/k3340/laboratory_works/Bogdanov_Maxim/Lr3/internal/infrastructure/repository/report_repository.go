package repository

import (
	"context"
	"database/sql"
	"fmt"

	"github.com/Masterminds/squirrel"
	"school-service/internal/domain/clock"
	"school-service/internal/domain/repository"
)

var _ repository.ReportRepository = (*ReportRepository)(nil)

// ReportRepository реализация репозитория для отчетов
type ReportRepository struct {
	db      *sql.DB
	builder squirrel.StatementBuilderType
	clock   clock.Clock
}

// NewReportRepository создает новый репозиторий для отчетов
func NewReportRepository(db *sql.DB, clock clock.Clock) *ReportRepository {
	return &ReportRepository{
		db:      db,
		builder: squirrel.StatementBuilder.PlaceholderFormat(squirrel.Dollar),
		clock:   clock,
	}
}

// GetClassInfo возвращает информацию о классе
func (r *ReportRepository) GetClassInfo(ctx context.Context, classID int) (*repository.ClassInfo, error) {
	query := r.builder.
		Select("id", "CONCAT(grade, letter) as name", "class_teacher_id").
		From("classes").
		Where(squirrel.Eq{"id": classID}).
		Where(squirrel.Expr("deleted_at IS NULL"))

	var info repository.ClassInfo
	var homeroomTeacherID sql.NullInt64

	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(
		&info.ID,
		&info.Name,
		&homeroomTeacherID,
	)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, fmt.Errorf("class not found: %w", err)
		}
		return nil, fmt.Errorf("failed to get class info: %w", err)
	}

	if homeroomTeacherID.Valid {
		id := int(homeroomTeacherID.Int64)
		info.HomeroomTeacherID = &id
	}

	return &info, nil
}

// GetStudentsCountByClass возвращает количество учеников в классе
func (r *ReportRepository) GetStudentsCountByClass(ctx context.Context, classID int) (int, error) {
	query := r.builder.
		Select("COUNT(*)").
		From("students").
		Where(squirrel.Eq{"class_id": classID}).
		Where(squirrel.Expr("deleted_at IS NULL"))

	var count int
	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(&count)
	if err != nil {
		return 0, fmt.Errorf("failed to get students count: %w", err)
	}

	return count, nil
}

// GetSubjectAverageGrades возвращает средние оценки по предметам для класса
func (r *ReportRepository) GetSubjectAverageGrades(ctx context.Context, classID int) ([]repository.SubjectAverageGrade, error) {
	query := r.builder.
		Select(
			"s.id",
			"s.name",
			"COALESCE(AVG(g.grade), 0) as average_grade",
			"COUNT(g.id) as grades_count",
		).
		From("grades g").
		Join("students st ON g.student_id = st.id").
		Join("subjects s ON g.subject_id = s.id").
		Where(squirrel.Eq{"st.class_id": classID}).
		Where(squirrel.Expr("st.deleted_at IS NULL")).
		GroupBy("s.id", "s.name").
		OrderBy("s.name")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get subject average grades: %w", err)
	}
	defer rows.Close()

	var results []repository.SubjectAverageGrade
	for rows.Next() {
		var result repository.SubjectAverageGrade
		if err := rows.Scan(
			&result.SubjectID,
			&result.SubjectName,
			&result.AverageGrade,
			&result.GradesCount,
		); err != nil {
			return nil, fmt.Errorf("failed to scan result: %w", err)
		}
		results = append(results, result)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate results: %w", err)
	}

	return results, nil
}

// GetOverallAverageGrade возвращает общий средний балл по классу
func (r *ReportRepository) GetOverallAverageGrade(ctx context.Context, classID int) (float64, error) {
	query := r.builder.
		Select("COALESCE(AVG(g.grade), 0)").
		From("grades g").
		Join("students st ON g.student_id = st.id").
		Where(squirrel.Eq{"st.class_id": classID}).
		Where(squirrel.Expr("st.deleted_at IS NULL"))

	var average float64
	err := query.RunWith(r.db).QueryRowContext(ctx).Scan(&average)
	if err != nil {
		return 0, fmt.Errorf("failed to get overall average grade: %w", err)
	}

	return average, nil
}
