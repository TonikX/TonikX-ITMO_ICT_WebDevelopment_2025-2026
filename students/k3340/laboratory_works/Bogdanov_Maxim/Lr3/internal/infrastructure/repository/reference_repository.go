package repository

import (
	"context"
	"database/sql"
	"time"

	"github.com/Masterminds/squirrel"
	"school-service/internal/domain"
	"school-service/internal/domain/repository"
)

var _ repository.ReferenceRepository = (*ReferenceRepository)(nil)

// ReferenceRepository реализация репозитория справочных данных
type ReferenceRepository struct {
	db      *sql.DB
	builder squirrel.StatementBuilderType
}

// NewReferenceRepository создает новый репозиторий справочных данных
func NewReferenceRepository(db *sql.DB) *ReferenceRepository {
	return &ReferenceRepository{
		db:      db,
		builder: squirrel.StatementBuilder.PlaceholderFormat(squirrel.Dollar),
	}
}

// GetAllSubjects возвращает все предметы
func (r *ReferenceRepository) GetAllSubjects(ctx context.Context) ([]*domain.Subject, error) {
	query := r.builder.
		Select("id", "name", "subject_type_id", "created_at", "updated_at").
		From("subjects").
		OrderBy("name")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var subjects []*domain.Subject
	for rows.Next() {
		var id, subjectTypeID int
		var name string
		var createdAt, updatedAt time.Time

		if err := rows.Scan(&id, &name, &subjectTypeID, &createdAt, &updatedAt); err != nil {
			return nil, err
		}

		subject := domain.RestoreSubjectFromDB(id, name, subjectTypeID, createdAt, updatedAt)
		subjects = append(subjects, subject)
	}

	return subjects, rows.Err()
}

// GetAllClassrooms возвращает все кабинеты
func (r *ReferenceRepository) GetAllClassrooms(ctx context.Context) ([]*domain.Classroom, error) {
	query := r.builder.
		Select("id", "room_number", "subject_type_id", "created_at", "updated_at").
		From("classrooms").
		OrderBy("room_number")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var classrooms []*domain.Classroom
	for rows.Next() {
		var id, subjectTypeID int
		var roomNumber string
		var createdAt, updatedAt time.Time

		if err := rows.Scan(&id, &roomNumber, &subjectTypeID, &createdAt, &updatedAt); err != nil {
			return nil, err
		}

		classroom := domain.RestoreClassroomFromDB(id, roomNumber, subjectTypeID, createdAt, updatedAt)
		classrooms = append(classrooms, classroom)
	}

	return classrooms, rows.Err()
}

// GetAllAcademicYears возвращает все учебные годы
func (r *ReferenceRepository) GetAllAcademicYears(ctx context.Context) ([]*domain.AcademicYear, error) {
	query := r.builder.
		Select("id", "name", "start_date", "end_date", "is_current", "created_at", "updated_at").
		From("academic_years").
		OrderBy("start_date DESC")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var academicYears []*domain.AcademicYear
	for rows.Next() {
		var ay domain.AcademicYear
		if err := rows.Scan(&ay.ID, &ay.Name, &ay.StartDate, &ay.EndDate, &ay.IsCurrent, &ay.CreatedAt, &ay.UpdatedAt); err != nil {
			return nil, err
		}
		academicYears = append(academicYears, &ay)
	}

	return academicYears, rows.Err()
}

// GetAllGradingPeriods возвращает все периоды оценивания
func (r *ReferenceRepository) GetAllGradingPeriods(ctx context.Context) ([]*domain.GradingPeriod, error) {
	query := r.builder.
		Select("id", "academic_year_id", "name", "period_order", "start_date", "end_date", "created_at", "updated_at").
		From("grading_periods").
		OrderBy("academic_year_id", "period_order")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var gradingPeriods []*domain.GradingPeriod
	for rows.Next() {
		var gp domain.GradingPeriod
		if err := rows.Scan(&gp.ID, &gp.AcademicYearID, &gp.Name, &gp.PeriodOrder, &gp.StartDate, &gp.EndDate, &gp.CreatedAt, &gp.UpdatedAt); err != nil {
			return nil, err
		}
		gradingPeriods = append(gradingPeriods, &gp)
	}

	return gradingPeriods, rows.Err()
}

// GetGradingPeriodsByAcademicYear возвращает периоды оценивания для учебного года
func (r *ReferenceRepository) GetGradingPeriodsByAcademicYear(ctx context.Context, academicYearID int) ([]*domain.GradingPeriod, error) {
	query := r.builder.
		Select("id", "academic_year_id", "name", "period_order", "start_date", "end_date", "created_at", "updated_at").
		From("grading_periods").
		Where(squirrel.Eq{"academic_year_id": academicYearID}).
		OrderBy("period_order")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var gradingPeriods []*domain.GradingPeriod
	for rows.Next() {
		var gp domain.GradingPeriod
		if err := rows.Scan(&gp.ID, &gp.AcademicYearID, &gp.Name, &gp.PeriodOrder, &gp.StartDate, &gp.EndDate, &gp.CreatedAt, &gp.UpdatedAt); err != nil {
			return nil, err
		}
		gradingPeriods = append(gradingPeriods, &gp)
	}

	return gradingPeriods, rows.Err()
}

// GetAllWeekdays возвращает все дни недели
func (r *ReferenceRepository) GetAllWeekdays(ctx context.Context) ([]*domain.Weekday, error) {
	query := r.builder.
		Select("id", "name", "day_order").
		From("weekdays").
		OrderBy("day_order")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var weekdays []*domain.Weekday
	for rows.Next() {
		var wd domain.Weekday
		if err := rows.Scan(&wd.ID, &wd.Name, &wd.DayOrder); err != nil {
			return nil, err
		}
		weekdays = append(weekdays, &wd)
	}

	return weekdays, rows.Err()
}
