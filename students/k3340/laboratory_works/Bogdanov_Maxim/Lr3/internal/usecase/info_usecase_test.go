package usecase

import (
	"context"
	"errors"
	"testing"
	"time"

	"school-service/internal/domain"
	mockclock "school-service/internal/infrastructure/clock"
)

// mockInfoRepository мок репозитория для информационных запросов
type mockInfoRepository struct {
	teachersCountBySubject map[string]int
	subjectIDsByTeacher    map[int][]int
	teacherIDsBySubjects   map[string][]int
	studentsCountByGender  map[int]map[string]int
	classroomsCountByType  map[string]int
	err                    error
}

func newMockInfoRepository() *mockInfoRepository {
	return &mockInfoRepository{
		teachersCountBySubject: make(map[string]int),
		subjectIDsByTeacher:    make(map[int][]int),
		teacherIDsBySubjects:   make(map[string][]int),
		studentsCountByGender:  make(map[int]map[string]int),
		classroomsCountByType:  make(map[string]int),
	}
}

func (m *mockInfoRepository) GetTeachersCountBySubject(ctx context.Context) (map[string]int, error) {
	if m.err != nil {
		return nil, m.err
	}
	return m.teachersCountBySubject, nil
}

func (m *mockInfoRepository) GetSubjectIDsByTeacher(ctx context.Context, teacherID int) ([]int, error) {
	if m.err != nil {
		return nil, m.err
	}
	return m.subjectIDsByTeacher[teacherID], nil
}

func (m *mockInfoRepository) GetTeacherIDsBySubjects(ctx context.Context, subjectIDs []int) ([]int, error) {
	if m.err != nil {
		return nil, m.err
	}
	key := ""
	for _, id := range subjectIDs {
		key += string(rune(id))
	}
	return m.teacherIDsBySubjects[key], nil
}

func (m *mockInfoRepository) GetStudentsCountByGender(ctx context.Context) (map[int]map[string]int, error) {
	if m.err != nil {
		return nil, m.err
	}
	return m.studentsCountByGender, nil
}

func (m *mockInfoRepository) GetClassroomsCountByType(ctx context.Context) (map[string]int, error) {
	if m.err != nil {
		return nil, m.err
	}
	return m.classroomsCountByType, nil
}

func TestInfoUseCase_GetTeachersCountBySubject(t *testing.T) {
	mockInfoRepo := newMockInfoRepository()
	mockTeacherRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	mockInfoRepo.teachersCountBySubject["Math"] = 5
	mockInfoRepo.teachersCountBySubject["Physics"] = 3

	uc := NewInfoUseCase(mockInfoRepo, mockTeacherRepo, mockLog)

	ctx := context.Background()
	result, err := uc.GetTeachersCountBySubject(ctx)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(result) != 2 {
		t.Errorf("expected 2 subjects, got %d", len(result))
	}

	if result["Math"] != 5 {
		t.Errorf("expected Math = 5, got %d", result["Math"])
	}
}

func TestInfoUseCase_GetTeachersBySameSubjects(t *testing.T) {
	mockClock := mockclock.NewMockClock(time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC))
	mockInfoRepo := newMockInfoRepository()
	mockTeacherRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	// Учитель 1 преподает предметы 1 и 2
	mockInfoRepo.subjectIDsByTeacher[1] = []int{1, 2}

	// Учителя 2 и 3 также преподают предметы 1 и 2
	key := string(rune(1)) + string(rune(2))
	mockInfoRepo.teacherIDsBySubjects[key] = []int{1, 2, 3}

	// Создаем учителей
	teacher2, _ := domain.NewTeacher(mockClock, "Jane", "Doe", nil, nil)
	teacher2.SetID(2)
	mockTeacherRepo.teachers[2] = teacher2

	teacher3, _ := domain.NewTeacher(mockClock, "Bob", "Smith", nil, nil)
	teacher3.SetID(3)
	mockTeacherRepo.teachers[3] = teacher3

	uc := NewInfoUseCase(mockInfoRepo, mockTeacherRepo, mockLog)

	ctx := context.Background()
	teachers, err := uc.GetTeachersBySameSubjects(ctx, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	// Должны вернуться учителя 2 и 3 (учитель 1 исключается)
	if len(teachers) != 2 {
		t.Errorf("expected 2 teachers, got %d", len(teachers))
	}
}

func TestInfoUseCase_GetTeachersBySameSubjects_NoSubjects(t *testing.T) {
	mockInfoRepo := newMockInfoRepository()
	mockTeacherRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	// Учитель не преподает никаких предметов
	mockInfoRepo.subjectIDsByTeacher[1] = []int{}

	uc := NewInfoUseCase(mockInfoRepo, mockTeacherRepo, mockLog)

	ctx := context.Background()
	teachers, err := uc.GetTeachersBySameSubjects(ctx, 1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(teachers) != 0 {
		t.Errorf("expected 0 teachers, got %d", len(teachers))
	}
}

func TestInfoUseCase_GetStudentsCountByGender(t *testing.T) {
	mockInfoRepo := newMockInfoRepository()
	mockTeacherRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	mockInfoRepo.studentsCountByGender[1] = map[string]int{
		"Male":   10,
		"Female": 12,
	}

	uc := NewInfoUseCase(mockInfoRepo, mockTeacherRepo, mockLog)

	ctx := context.Background()
	result, err := uc.GetStudentsCountByGender(ctx)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(result) != 1 {
		t.Errorf("expected 1 class, got %d", len(result))
	}

	if result[1]["Male"] != 10 {
		t.Errorf("expected Male = 10, got %d", result[1]["Male"])
	}
}

func TestInfoUseCase_GetClassroomsCountByType(t *testing.T) {
	mockInfoRepo := newMockInfoRepository()
	mockTeacherRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	mockInfoRepo.classroomsCountByType["Basic"] = 15
	mockInfoRepo.classroomsCountByType["Advanced"] = 8

	uc := NewInfoUseCase(mockInfoRepo, mockTeacherRepo, mockLog)

	ctx := context.Background()
	result, err := uc.GetClassroomsCountByType(ctx)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(result) != 2 {
		t.Errorf("expected 2 types, got %d", len(result))
	}

	if result["Basic"] != 15 {
		t.Errorf("expected Basic = 15, got %d", result["Basic"])
	}
}

func TestInfoUseCase_GetTeachersCountBySubject_Error(t *testing.T) {
	mockInfoRepo := newMockInfoRepository()
	mockTeacherRepo := newMockTeacherRepository()
	mockLog := &mockLogger{}

	mockInfoRepo.err = errors.New("database error")

	uc := NewInfoUseCase(mockInfoRepo, mockTeacherRepo, mockLog)

	ctx := context.Background()
	_, err := uc.GetTeachersCountBySubject(ctx)
	if err == nil {
		t.Error("expected error")
	}
}
