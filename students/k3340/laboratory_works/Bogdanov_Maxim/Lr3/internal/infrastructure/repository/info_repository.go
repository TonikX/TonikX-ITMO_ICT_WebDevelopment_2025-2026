package repository

import (
	"context"
	"database/sql"
	"fmt"

	"github.com/Masterminds/squirrel"
	"school-service/internal/domain/clock"
	"school-service/internal/domain/repository"
)

var _ repository.InfoRepository = (*InfoRepository)(nil)

// InfoRepository реализация репозитория для информационных запросов
type InfoRepository struct {
	db      *sql.DB
	builder squirrel.StatementBuilderType
	clock   clock.Clock
}

// NewInfoRepository создает новый репозиторий для информационных запросов
func NewInfoRepository(db *sql.DB, clock clock.Clock) *InfoRepository {
	return &InfoRepository{
		db:      db,
		builder: squirrel.StatementBuilder.PlaceholderFormat(squirrel.Dollar),
		clock:   clock,
	}
}

// GetTeachersCountBySubject возвращает количество учителей по каждому предмету
func (r *InfoRepository) GetTeachersCountBySubject(ctx context.Context) (map[string]int, error) {
	query := r.builder.
		Select("s.name", "COUNT(DISTINCT ts.teacher_id)").
		From("teacher_subjects ts").
		Join("subjects s ON ts.subject_id = s.id").
		Where(squirrel.Expr("ts.end_date IS NULL")).
		GroupBy("s.name").
		OrderBy("s.name")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get teachers count by subject: %w", err)
	}
	defer rows.Close()

	result := make(map[string]int)
	for rows.Next() {
		var subjectName string
		var count int
		if err := rows.Scan(&subjectName, &count); err != nil {
			return nil, fmt.Errorf("failed to scan result: %w", err)
		}
		result[subjectName] = count
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate results: %w", err)
	}

	return result, nil
}

// GetSubjectIDsByTeacher возвращает список ID предметов, которые преподает учитель
func (r *InfoRepository) GetSubjectIDsByTeacher(ctx context.Context, teacherID int) ([]int, error) {
	query := r.builder.
		Select("subject_id").
		From("teacher_subjects").
		Where(squirrel.Eq{"teacher_id": teacherID}).
		Where(squirrel.Expr("end_date IS NULL"))

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get subject IDs by teacher: %w", err)
	}
	defer rows.Close()

	var subjectIDs []int
	for rows.Next() {
		var subjectID int
		if err := rows.Scan(&subjectID); err != nil {
			return nil, fmt.Errorf("failed to scan subject ID: %w", err)
		}
		subjectIDs = append(subjectIDs, subjectID)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate results: %w", err)
	}

	return subjectIDs, nil
}

// GetTeacherIDsBySubjects возвращает список ID учителей, которые преподают ВСЕ указанные предметы
func (r *InfoRepository) GetTeacherIDsBySubjects(ctx context.Context, subjectIDs []int) ([]int, error) {
	if len(subjectIDs) == 0 {
		return []int{}, nil
	}

	query := r.builder.
		Select("teacher_id").
		From("teacher_subjects").
		Where(squirrel.Eq{"subject_id": subjectIDs}).
		Where(squirrel.Expr("end_date IS NULL")).
		GroupBy("teacher_id").
		Having(fmt.Sprintf("COUNT(DISTINCT subject_id) = %d", len(subjectIDs)))

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get teacher IDs by subjects: %w", err)
	}
	defer rows.Close()

	var teacherIDs []int
	for rows.Next() {
		var teacherID int
		if err := rows.Scan(&teacherID); err != nil {
			return nil, fmt.Errorf("failed to scan teacher ID: %w", err)
		}
		teacherIDs = append(teacherIDs, teacherID)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate results: %w", err)
	}

	return teacherIDs, nil
}

// GetStudentsCountByGender возвращает количество мальчиков и девочек в каждом классе
func (r *InfoRepository) GetStudentsCountByGender(ctx context.Context) (map[int]map[string]int, error) {
	query := r.builder.
		Select("s.class_id", "g.name", "COUNT(*)").
		From("students s").
		Join("genders g ON s.gender_id = g.id").
		Where(squirrel.Expr("s.deleted_at IS NULL")).
		GroupBy("s.class_id", "g.name").
		OrderBy("s.class_id", "g.name")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get students count by gender: %w", err)
	}
	defer rows.Close()

	result := make(map[int]map[string]int)
	for rows.Next() {
		var classID int
		var genderName string
		var count int
		if err := rows.Scan(&classID, &genderName, &count); err != nil {
			return nil, fmt.Errorf("failed to scan result: %w", err)
		}

		if result[classID] == nil {
			result[classID] = make(map[string]int)
		}
		result[classID][genderName] = count
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate results: %w", err)
	}

	return result, nil
}

// GetClassroomsCountByType возвращает количество кабинетов по типам дисциплин
func (r *InfoRepository) GetClassroomsCountByType(ctx context.Context) (map[string]int, error) {
	query := r.builder.
		Select("st.name", "COUNT(*)").
		From("classrooms c").
		Join("subject_types st ON c.subject_type_id = st.id").
		GroupBy("st.name").
		OrderBy("st.name")

	rows, err := query.RunWith(r.db).QueryContext(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get classrooms count by type: %w", err)
	}
	defer rows.Close()

	result := make(map[string]int)
	for rows.Next() {
		var typeName string
		var count int
		if err := rows.Scan(&typeName, &count); err != nil {
			return nil, fmt.Errorf("failed to scan result: %w", err)
		}
		result[typeName] = count
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed to iterate results: %w", err)
	}

	return result, nil
}
