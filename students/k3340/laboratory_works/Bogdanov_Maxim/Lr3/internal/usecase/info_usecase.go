package usecase

import (
	"context"
	"fmt"

	"school-service/internal/domain"
	"school-service/internal/domain/logger"
	"school-service/internal/domain/repository"
	"school-service/internal/domain/usecase"
)

var _ usecase.InfoUseCase = (*InfoUseCase)(nil)

// InfoUseCase реализация бизнес-логики для информационных запросов
type InfoUseCase struct {
	infoRepo    repository.InfoRepository
	teacherRepo repository.TeacherRepository
	logger      logger.Logger
}

// NewInfoUseCase создает новый usecase для информационных запросов
func NewInfoUseCase(infoRepo repository.InfoRepository, teacherRepo repository.TeacherRepository, logger logger.Logger) *InfoUseCase {
	return &InfoUseCase{
		infoRepo:    infoRepo,
		teacherRepo: teacherRepo,
		logger:      logger,
	}
}

// GetTeachersCountBySubject возвращает количество учителей по каждому предмету
func (u *InfoUseCase) GetTeachersCountBySubject(ctx context.Context) (map[string]int, error) {
	result, err := u.infoRepo.GetTeachersCountBySubject(ctx)
	if err != nil {
		u.logger.Error("Failed to get teachers count by subject", "error", err)
		return nil, fmt.Errorf("failed to get teachers count by subject: %w", err)
	}

	return result, nil
}

// GetTeachersBySameSubjects возвращает учителей, преподающих те же предметы, что и указанный учитель
func (u *InfoUseCase) GetTeachersBySameSubjects(ctx context.Context, teacherID int) ([]*domain.Teacher, error) {
	// Получаем предметы, которые преподает указанный учитель
	subjectIDs, err := u.infoRepo.GetSubjectIDsByTeacher(ctx, teacherID)
	if err != nil {
		u.logger.Error("Failed to get subject IDs by teacher", "error", err, "teacherID", teacherID)
		return nil, fmt.Errorf("failed to get subject IDs by teacher: %w", err)
	}

	if len(subjectIDs) == 0 {
		return []*domain.Teacher{}, nil
	}

	// Получаем учителей, которые преподают те же предметы
	teacherIDs, err := u.infoRepo.GetTeacherIDsBySubjects(ctx, subjectIDs)
	if err != nil {
		u.logger.Error("Failed to get teacher IDs by subjects", "error", err, "subjectIDs", subjectIDs)
		return nil, fmt.Errorf("failed to get teacher IDs by subjects: %w", err)
	}

	// Исключаем самого учителя из результата
	var filteredTeacherIDs []int
	for _, id := range teacherIDs {
		if id != teacherID {
			filteredTeacherIDs = append(filteredTeacherIDs, id)
		}
	}

	// Получаем данные учителей
	var teachers []*domain.Teacher
	for _, id := range filteredTeacherIDs {
		teacher, err := u.teacherRepo.GetByIDActive(ctx, id)
		if err != nil {
			u.logger.Warn("Failed to get teacher", "error", err, "teacherID", id)
			continue
		}
		teachers = append(teachers, teacher)
	}

	return teachers, nil
}

// GetStudentsCountByGender возвращает количество мальчиков и девочек в каждом классе
func (u *InfoUseCase) GetStudentsCountByGender(ctx context.Context) (map[int]map[string]int, error) {
	result, err := u.infoRepo.GetStudentsCountByGender(ctx)
	if err != nil {
		u.logger.Error("Failed to get students count by gender", "error", err)
		return nil, fmt.Errorf("failed to get students count by gender: %w", err)
	}

	return result, nil
}

// GetClassroomsCountByType возвращает количество кабинетов базовых и профильных дисциплин
func (u *InfoUseCase) GetClassroomsCountByType(ctx context.Context) (map[string]int, error) {
	result, err := u.infoRepo.GetClassroomsCountByType(ctx)
	if err != nil {
		u.logger.Error("Failed to get classrooms count by type", "error", err)
		return nil, fmt.Errorf("failed to get classrooms count by type: %w", err)
	}

	return result, nil
}
