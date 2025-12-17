package usecase

import (
	"context"

	"school-service/internal/domain"
)

// InfoUseCase интерфейс для информационных запросов
type InfoUseCase interface {
	// GetTeachersCountBySubject возвращает количество учителей по каждому предмету
	GetTeachersCountBySubject(ctx context.Context) (map[string]int, error)

	// GetTeachersBySameSubjects возвращает учителей, преподающих те же предметы, что и указанный учитель
	GetTeachersBySameSubjects(ctx context.Context, teacherID int) ([]*domain.Teacher, error)

	// GetStudentsCountByGender возвращает количество мальчиков и девочек в каждом классе
	GetStudentsCountByGender(ctx context.Context) (map[int]map[string]int, error)

	// GetClassroomsCountByType возвращает количество кабинетов базовых и профильных дисциплин
	GetClassroomsCountByType(ctx context.Context) (map[string]int, error)
}
