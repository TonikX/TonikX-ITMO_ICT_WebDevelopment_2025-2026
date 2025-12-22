package repository

import (
	"context"
)

// InfoRepository интерфейс для информационных запросов
type InfoRepository interface {
	// GetTeachersCountBySubject возвращает количество учителей по каждому предмету
	GetTeachersCountBySubject(ctx context.Context) (map[string]int, error)

	// GetSubjectIDsByTeacher возвращает список ID предметов, которые преподает учитель
	GetSubjectIDsByTeacher(ctx context.Context, teacherID int) ([]int, error)

	// GetTeacherIDsBySubjects возвращает список ID учителей, которые преподают указанные предметы
	GetTeacherIDsBySubjects(ctx context.Context, subjectIDs []int) ([]int, error)

	// GetStudentsCountByGender возвращает количество мальчиков и девочек в каждом классе
	GetStudentsCountByGender(ctx context.Context) (map[int]map[string]int, error)

	// GetClassroomsCountByType возвращает количество кабинетов по типам дисциплин
	GetClassroomsCountByType(ctx context.Context) (map[string]int, error)
}
