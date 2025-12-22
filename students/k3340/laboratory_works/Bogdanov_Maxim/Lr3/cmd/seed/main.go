package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"

	_ "github.com/lib/pq"
	"golang.org/x/crypto/bcrypt"
)

func main() {
	// Получаем параметры подключения из переменных окружения или используем значения по умолчанию
	dbHost := getEnv("DB_HOST", "localhost")
	dbPort := getEnv("DB_PORT", "5432")
	dbUser := getEnv("DB_USER", "postgres")
	dbPassword := getEnv("DB_PASSWORD", "postgres")
	dbName := getEnv("DB_NAME", "school_db")
	dbSSLMode := getEnv("DB_SSLMODE", "disable")

	log.Printf("Connecting to database: host=%s port=%s user=%s dbname=%s", dbHost, dbPort, dbUser, dbName)

	// Подключаемся к нужной БД
	dsn := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=%s",
		dbHost, dbPort, dbUser, dbPassword, dbName, dbSSLMode)

	db, err := sql.Open("postgres", dsn)
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	defer db.Close()

	if err := db.Ping(); err != nil {
		log.Fatalf("Failed to ping database: %v", err)
	}

	log.Println("Connected to database successfully")

	// Заполняем справочники
	if err := seedReferenceData(db); err != nil {
		log.Fatalf("Failed to seed reference data: %v", err)
	}

	// Заполняем основные данные
	if err := seedMainData(db); err != nil {
		log.Fatalf("Failed to seed main data: %v", err)
	}

	log.Println("Database seeded successfully!")
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func seedReferenceData(db *sql.DB) error {
	log.Println("Seeding reference data...")

	// Пол
	_, err := db.Exec(`
		INSERT INTO genders (id, name) VALUES
		(1, 'Мужской'),
		(2, 'Женский')
		ON CONFLICT (id) DO NOTHING
	`)
	if err != nil {
		return fmt.Errorf("failed to seed genders: %w", err)
	}

	// Дни недели
	_, err = db.Exec(`
		INSERT INTO weekdays (id, name, day_order) VALUES
		(1, 'Понедельник', 1),
		(2, 'Вторник', 2),
		(3, 'Среда', 3),
		(4, 'Четверг', 4),
		(5, 'Пятница', 5),
		(6, 'Суббота', 6),
		(7, 'Воскресенье', 7)
		ON CONFLICT (id) DO NOTHING
	`)
	if err != nil {
		return fmt.Errorf("failed to seed weekdays: %w", err)
	}

	// Типы предметов
	_, err = db.Exec(`
		INSERT INTO subject_types (id, name) VALUES
		(1, 'Гуманитарный'),
		(2, 'Естественно-научный'),
		(3, 'Математический'),
		(4, 'Иностранный язык'),
		(5, 'Физкультура'),
		(6, 'Искусство')
		ON CONFLICT (id) DO NOTHING
	`)
	if err != nil {
		return fmt.Errorf("failed to seed subject_types: %w", err)
	}

	// Учебные годы
	_, err = db.Exec(`
		INSERT INTO academic_years (id, name, start_date, end_date, is_current) VALUES
		(1, '2023-2024', '2023-09-01', '2024-05-31', false),
		(2, '2024-2025', '2024-09-01', '2025-05-31', true)
		ON CONFLICT (id) DO NOTHING
	`)
	if err != nil {
		return fmt.Errorf("failed to seed academic_years: %w", err)
	}

	// Периоды оценивания для 2024-2025
	_, err = db.Exec(`
		INSERT INTO grading_periods (id, academic_year_id, name, period_order, start_date, end_date) VALUES
		(1, 2, '1 четверть', 1, '2024-09-01', '2024-10-26'),
		(2, 2, '2 четверть', 2, '2024-11-05', '2024-12-28'),
		(3, 2, '3 четверть', 3, '2025-01-09', '2025-03-22'),
		(4, 2, '4 четверть', 4, '2025-03-31', '2025-05-31')
		ON CONFLICT (id) DO NOTHING
	`)
	if err != nil {
		return fmt.Errorf("failed to seed grading_periods: %w", err)
	}

	// Предметы
	_, err = db.Exec(`
		INSERT INTO subjects (id, name, subject_type_id) VALUES
		(1, 'Русский язык', 1),
		(2, 'Литература', 1),
		(3, 'Математика', 3),
		(4, 'Алгебра', 3),
		(5, 'Геометрия', 3),
		(6, 'Физика', 2),
		(7, 'Химия', 2),
		(8, 'Биология', 2),
		(9, 'История', 1),
		(10, 'Обществознание', 1),
		(11, 'География', 2),
		(12, 'Английский язык', 4),
		(13, 'Физкультура', 5),
		(14, 'Информатика', 3),
		(15, 'Музыка', 6),
		(16, 'ИЗО', 6)
		ON CONFLICT (id) DO NOTHING
	`)
	if err != nil {
		return fmt.Errorf("failed to seed subjects: %w", err)
	}

	// Кабинеты
	_, err = db.Exec(`
		INSERT INTO classrooms (id, room_number, subject_type_id) VALUES
		(1, '101', 1),
		(2, '102', 1),
		(3, '201', 3),
		(4, '202', 3),
		(5, '301', 2),
		(6, '302', 2),
		(7, '401', 4),
		(8, '402', 4),
		(9, '501', 5),
		(10, '502', 5),
		(11, '601', 6),
		(12, '602', 6),
		(13, '103', 1),
		(14, '203', 3),
		(15, '303', 2)
		ON CONFLICT (id) DO NOTHING
	`)
	if err != nil {
		return fmt.Errorf("failed to seed classrooms: %w", err)
	}

	log.Println("Reference data seeded successfully")
	return nil
}

func seedMainData(db *sql.DB) error {
	log.Println("Seeding main data...")

	// Учителя
	teachers := []struct {
		firstName   string
		lastName    string
		middleName  *string
		classroomID *int
	}{
		{"Иван", "Иванов", strPtr("Петрович"), intPtr(1)},
		{"Мария", "Петрова", strPtr("Сергеевна"), intPtr(2)},
		{"Александр", "Сидоров", strPtr("Александрович"), intPtr(3)},
		{"Елена", "Козлова", strPtr("Владимировна"), intPtr(4)},
		{"Дмитрий", "Смирнов", strPtr("Игоревич"), intPtr(5)},
		{"Ольга", "Волкова", strPtr("Николаевна"), intPtr(6)},
		{"Сергей", "Лебедев", strPtr("Андреевич"), intPtr(7)},
		{"Анна", "Новикова", strPtr("Дмитриевна"), intPtr(8)},
		{"Павел", "Морозов", strPtr("Викторович"), intPtr(9)},
		{"Татьяна", "Федорова", strPtr("Ивановна"), intPtr(10)},
	}

	var teacherIDs []int
	for _, t := range teachers {
		var id int
		err := db.QueryRow(`
			INSERT INTO teachers (first_name, last_name, middle_name, classroom_id)
			VALUES ($1, $2, $3, $4)
			ON CONFLICT DO NOTHING
			RETURNING id
		`, t.firstName, t.lastName, t.middleName, t.classroomID).Scan(&id)
		if err == sql.ErrNoRows {
			// Если конфликт, получаем существующий ID
			err = db.QueryRow(`
				SELECT id FROM teachers 
				WHERE first_name = $1 AND last_name = $2 AND (middle_name = $3 OR (middle_name IS NULL AND $3 IS NULL))
			`, t.firstName, t.lastName, t.middleName).Scan(&id)
			if err != nil {
				return fmt.Errorf("failed to get teacher ID: %w", err)
			}
		} else if err != nil {
			return fmt.Errorf("failed to insert teacher: %w", err)
		}
		teacherIDs = append(teacherIDs, id)
	}

	// Связь учителей и предметов
	teacherSubjects := []struct {
		teacherID int
		subjectID int
	}{
		{teacherIDs[0], 1},  // Иванов - Русский язык
		{teacherIDs[0], 2},  // Иванов - Литература
		{teacherIDs[1], 3},  // Петрова - Математика
		{teacherIDs[1], 4},  // Петрова - Алгебра
		{teacherIDs[2], 5},  // Сидоров - Геометрия
		{teacherIDs[3], 6},  // Козлова - Физика
		{teacherIDs[4], 7},  // Смирнов - Химия
		{teacherIDs[5], 8},  // Волкова - Биология
		{teacherIDs[6], 9},  // Лебедев - История
		{teacherIDs[6], 10}, // Лебедев - Обществознание
		{teacherIDs[7], 11}, // Новикова - География
		{teacherIDs[8], 12}, // Морозов - Английский язык
		{teacherIDs[9], 13}, // Федорова - Физкультура
		{teacherIDs[2], 14}, // Сидоров - Информатика
		{teacherIDs[7], 15}, // Новикова - Музыка
		{teacherIDs[7], 16}, // Новикова - ИЗО
	}

	for _, ts := range teacherSubjects {
		_, err := db.Exec(`
			INSERT INTO teacher_subjects (teacher_id, subject_id, start_date)
			VALUES ($1, $2, $3)
			ON CONFLICT DO NOTHING
		`, ts.teacherID, ts.subjectID, "2024-09-01")
		if err != nil {
			return fmt.Errorf("failed to seed teacher_subjects: %w", err)
		}
	}

	// Классы
	classes := []struct {
		grade          int
		letter         string
		academicYearID int
		classTeacherID *int
	}{
		{9, "A", 2, &teacherIDs[0]},
		{9, "B", 2, &teacherIDs[1]},
		{10, "A", 2, &teacherIDs[2]},
		{10, "B", 2, &teacherIDs[3]},
		{11, "A", 2, &teacherIDs[4]},
	}

	var classIDs []int
	for _, c := range classes {
		var id int
		err := db.QueryRow(`
			INSERT INTO classes (grade, letter, academic_year_id, class_teacher_id)
			VALUES ($1, $2, $3, $4)
			ON CONFLICT DO NOTHING
			RETURNING id
		`, c.grade, c.letter, c.academicYearID, c.classTeacherID).Scan(&id)
		if err == sql.ErrNoRows {
			err = db.QueryRow(`
				SELECT id FROM classes 
				WHERE grade = $1 AND letter = $2 AND academic_year_id = $3
			`, c.grade, c.letter, c.academicYearID).Scan(&id)
			if err != nil {
				return fmt.Errorf("failed to get class ID: %w", err)
			}
		} else if err != nil {
			return fmt.Errorf("failed to insert class: %w", err)
		}
		classIDs = append(classIDs, id)
	}

	// Ученики
	students := []struct {
		firstName  string
		lastName   string
		middleName *string
		genderID   int
		classID    int
	}{
		// 9A
		{"Алексей", "Алексеев", strPtr("Алексеевич"), 1, classIDs[0]},
		{"Дмитрий", "Дмитриев", strPtr("Дмитриевич"), 1, classIDs[0]},
		{"Максим", "Максимов", strPtr("Максимович"), 1, classIDs[0]},
		{"Анна", "Аннова", strPtr("Анновна"), 2, classIDs[0]},
		{"Елена", "Еленова", strPtr("Еленовна"), 2, classIDs[0]},
		{"Мария", "Маринова", strPtr("Мариновна"), 2, classIDs[0]},
		// 9B
		{"Иван", "Иванов", strPtr("Иванович"), 1, classIDs[1]},
		{"Петр", "Петров", strPtr("Петрович"), 1, classIDs[1]},
		{"Сергей", "Сергеев", strPtr("Сергеевич"), 1, classIDs[1]},
		{"Ольга", "Ольгова", strPtr("Ольговна"), 2, classIDs[1]},
		{"Татьяна", "Татьянова", strPtr("Татьяновна"), 2, classIDs[1]},
		{"Юлия", "Юльева", strPtr("Юльевна"), 2, classIDs[1]},
		// 10A
		{"Андрей", "Андреев", strPtr("Андреевич"), 1, classIDs[2]},
		{"Владимир", "Владимиров", strPtr("Владимирович"), 1, classIDs[2]},
		{"Николай", "Николаев", strPtr("Николаевич"), 1, classIDs[2]},
		{"Екатерина", "Екатеринова", strPtr("Екатериновна"), 2, classIDs[2]},
		{"Ирина", "Иринова", strPtr("Ириновна"), 2, classIDs[2]},
		{"Наталья", "Натальева", strPtr("Натальевна"), 2, classIDs[2]},
		// 10B
		{"Артем", "Артемов", strPtr("Артемович"), 1, classIDs[3]},
		{"Борис", "Борисов", strPtr("Борисович"), 1, classIDs[3]},
		{"Григорий", "Григорьев", strPtr("Григорьевич"), 1, classIDs[3]},
		{"Виктория", "Викторова", strPtr("Викторовна"), 2, classIDs[3]},
		{"Дарья", "Дарьева", strPtr("Дарьевна"), 2, classIDs[3]},
		{"Ксения", "Ксенева", strPtr("Ксеневна"), 2, classIDs[3]},
		// 11A
		{"Роман", "Романов", strPtr("Романович"), 1, classIDs[4]},
		{"Станислав", "Станиславов", strPtr("Станиславович"), 1, classIDs[4]},
		{"Тимур", "Тимуров", strPtr("Тимурович"), 1, classIDs[4]},
		{"Алиса", "Алисова", strPtr("Алисовна"), 2, classIDs[4]},
		{"Валерия", "Валерьева", strPtr("Валерьевна"), 2, classIDs[4]},
		{"София", "Софьева", strPtr("Софьевна"), 2, classIDs[4]},
	}

	var studentIDs []int
	for _, s := range students {
		var id int
		err := db.QueryRow(`
			INSERT INTO students (first_name, last_name, middle_name, gender_id, class_id)
			VALUES ($1, $2, $3, $4, $5)
			ON CONFLICT DO NOTHING
			RETURNING id
		`, s.firstName, s.lastName, s.middleName, s.genderID, s.classID).Scan(&id)
		if err == sql.ErrNoRows {
			err = db.QueryRow(`
				SELECT id FROM students 
				WHERE first_name = $1 AND last_name = $2 AND class_id = $5
			`, s.firstName, s.lastName, s.classID).Scan(&id)
			if err != nil {
				return fmt.Errorf("failed to get student ID: %w", err)
			}
		} else if err != nil {
			return fmt.Errorf("failed to insert student: %w", err)
		}
		studentIDs = append(studentIDs, id)
	}

	// Расписание для всех классов
	schedules := []struct {
		classID      int
		weekdayID    int
		lessonNumber int
		subjectID    int
		teacherID    int
		classroomID  int
	}{
		// 9A - Понедельник
		{classIDs[0], 1, 1, 1, teacherIDs[0], 1},  // Русский язык
		{classIDs[0], 1, 2, 3, teacherIDs[1], 3},  // Математика
		{classIDs[0], 1, 3, 6, teacherIDs[3], 5},  // Физика
		{classIDs[0], 1, 4, 12, teacherIDs[8], 7}, // Английский
		{classIDs[0], 1, 5, 13, teacherIDs[9], 9}, // Физкультура
		// 9A - Вторник
		{classIDs[0], 2, 1, 2, teacherIDs[0], 1},  // Литература
		{classIDs[0], 2, 2, 4, teacherIDs[1], 3},  // Алгебра
		{classIDs[0], 2, 3, 8, teacherIDs[5], 5},  // Биология
		{classIDs[0], 2, 4, 9, teacherIDs[6], 2},  // История
		{classIDs[0], 2, 5, 12, teacherIDs[8], 7}, // Английский
		// 9A - Среда
		{classIDs[0], 3, 1, 1, teacherIDs[0], 1},  // Русский
		{classIDs[0], 3, 2, 5, teacherIDs[2], 4},  // Геометрия
		{classIDs[0], 3, 3, 11, teacherIDs[7], 6}, // География
		{classIDs[0], 3, 4, 14, teacherIDs[2], 4}, // Информатика
		{classIDs[0], 3, 5, 13, teacherIDs[9], 9}, // Физкультура
		// 9A - Четверг
		{classIDs[0], 4, 1, 3, teacherIDs[1], 3},   // Математика
		{classIDs[0], 4, 2, 7, teacherIDs[4], 5},   // Химия
		{classIDs[0], 4, 3, 10, teacherIDs[6], 2},  // Обществознание
		{classIDs[0], 4, 4, 12, teacherIDs[8], 7},  // Английский
		{classIDs[0], 4, 5, 15, teacherIDs[7], 11}, // Музыка
		// 9A - Пятница
		{classIDs[0], 5, 1, 2, teacherIDs[0], 1},   // Литература
		{classIDs[0], 5, 2, 4, teacherIDs[1], 3},   // Алгебра
		{classIDs[0], 5, 3, 6, teacherIDs[3], 5},   // Физика
		{classIDs[0], 5, 4, 9, teacherIDs[6], 2},   // История
		{classIDs[0], 5, 5, 16, teacherIDs[7], 11}, // ИЗО

		// 9B - Понедельник
		{classIDs[1], 1, 1, 1, teacherIDs[0], 1},
		{classIDs[1], 1, 2, 3, teacherIDs[1], 3},
		{classIDs[1], 1, 3, 6, teacherIDs[3], 5},
		{classIDs[1], 1, 4, 12, teacherIDs[8], 7},
		{classIDs[1], 1, 5, 13, teacherIDs[9], 9},
		// 9B - Вторник
		{classIDs[1], 2, 1, 2, teacherIDs[0], 1},
		{classIDs[1], 2, 2, 4, teacherIDs[1], 3},
		{classIDs[1], 2, 3, 8, teacherIDs[5], 5},
		{classIDs[1], 2, 4, 9, teacherIDs[6], 2},
		{classIDs[1], 2, 5, 12, teacherIDs[8], 7},

		// 10A - Понедельник
		{classIDs[2], 1, 1, 1, teacherIDs[0], 1},
		{classIDs[2], 1, 2, 3, teacherIDs[1], 3},
		{classIDs[2], 1, 3, 6, teacherIDs[3], 5},
		{classIDs[2], 1, 4, 12, teacherIDs[8], 7},
		{classIDs[2], 1, 5, 13, teacherIDs[9], 9},

		// 10B - Понедельник
		{classIDs[3], 1, 1, 1, teacherIDs[0], 1},
		{classIDs[3], 1, 2, 3, teacherIDs[1], 3},
		{classIDs[3], 1, 3, 6, teacherIDs[3], 5},
		{classIDs[3], 1, 4, 12, teacherIDs[8], 7},
		{classIDs[3], 1, 5, 13, teacherIDs[9], 9},

		// 11A - Понедельник
		{classIDs[4], 1, 1, 1, teacherIDs[0], 1},
		{classIDs[4], 1, 2, 3, teacherIDs[1], 3},
		{classIDs[4], 1, 3, 6, teacherIDs[3], 5},
		{classIDs[4], 1, 4, 12, teacherIDs[8], 7},
		{classIDs[4], 1, 5, 13, teacherIDs[9], 9},
	}

	for _, s := range schedules {
		_, err := db.Exec(`
			INSERT INTO schedule (class_id, weekday_id, lesson_number, subject_id, teacher_id, classroom_id)
			VALUES ($1, $2, $3, $4, $5, $6)
			ON CONFLICT DO NOTHING
		`, s.classID, s.weekdayID, s.lessonNumber, s.subjectID, s.teacherID, s.classroomID)
		if err != nil {
			return fmt.Errorf("failed to seed schedule: %w", err)
		}
	}

	// Оценки для всех учеников по основным предметам
	grades := []struct {
		studentID       int
		subjectID       int
		gradingPeriodID int
		grade           int
	}{
		// 9A - все ученики, основные предметы, 1 и 2 четверти
		{studentIDs[0], 1, 1, 5}, {studentIDs[0], 1, 2, 5}, // Русский
		{studentIDs[0], 3, 1, 4}, {studentIDs[0], 3, 2, 5}, // Математика
		{studentIDs[0], 6, 1, 5}, {studentIDs[0], 6, 2, 4}, // Физика
		{studentIDs[0], 12, 1, 4}, {studentIDs[0], 12, 2, 5}, // Английский
		{studentIDs[1], 1, 1, 4}, {studentIDs[1], 1, 2, 4},
		{studentIDs[1], 3, 1, 3}, {studentIDs[1], 3, 2, 4},
		{studentIDs[1], 6, 1, 4}, {studentIDs[1], 6, 2, 4},
		{studentIDs[1], 12, 1, 3}, {studentIDs[1], 12, 2, 4},
		{studentIDs[2], 1, 1, 3}, {studentIDs[2], 1, 2, 4},
		{studentIDs[2], 3, 1, 3}, {studentIDs[2], 3, 2, 3},
		{studentIDs[2], 6, 1, 3}, {studentIDs[2], 6, 2, 3},
		{studentIDs[2], 12, 1, 3}, {studentIDs[2], 12, 2, 4},
		{studentIDs[3], 1, 1, 5}, {studentIDs[3], 1, 2, 5},
		{studentIDs[3], 3, 1, 5}, {studentIDs[3], 3, 2, 5},
		{studentIDs[3], 6, 1, 4}, {studentIDs[3], 6, 2, 5},
		{studentIDs[3], 12, 1, 5}, {studentIDs[3], 12, 2, 5},
		{studentIDs[4], 1, 1, 4}, {studentIDs[4], 1, 2, 4},
		{studentIDs[4], 3, 1, 4}, {studentIDs[4], 3, 2, 4},
		{studentIDs[4], 6, 1, 4}, {studentIDs[4], 6, 2, 4},
		{studentIDs[4], 12, 1, 4}, {studentIDs[4], 12, 2, 4},
		{studentIDs[5], 1, 1, 5}, {studentIDs[5], 1, 2, 5},
		{studentIDs[5], 3, 1, 5}, {studentIDs[5], 3, 2, 5},
		{studentIDs[5], 6, 1, 5}, {studentIDs[5], 6, 2, 5},
		{studentIDs[5], 12, 1, 5}, {studentIDs[5], 12, 2, 5},

		// 9B
		{studentIDs[6], 1, 1, 5}, {studentIDs[6], 1, 2, 5},
		{studentIDs[6], 3, 1, 5}, {studentIDs[6], 3, 2, 5},
		{studentIDs[6], 6, 1, 4}, {studentIDs[6], 6, 2, 5},
		{studentIDs[6], 12, 1, 5}, {studentIDs[6], 12, 2, 5},
		{studentIDs[7], 1, 1, 4}, {studentIDs[7], 1, 2, 4},
		{studentIDs[7], 3, 1, 4}, {studentIDs[7], 3, 2, 4},
		{studentIDs[7], 6, 1, 4}, {studentIDs[7], 6, 2, 4},
		{studentIDs[7], 12, 1, 4}, {studentIDs[7], 12, 2, 4},
		{studentIDs[8], 1, 1, 3}, {studentIDs[8], 1, 2, 4},
		{studentIDs[8], 3, 1, 3}, {studentIDs[8], 3, 2, 3},
		{studentIDs[8], 6, 1, 3}, {studentIDs[8], 6, 2, 4},
		{studentIDs[8], 12, 1, 3}, {studentIDs[8], 12, 2, 4},
		{studentIDs[9], 1, 1, 5}, {studentIDs[9], 1, 2, 5},
		{studentIDs[9], 3, 1, 5}, {studentIDs[9], 3, 2, 5},
		{studentIDs[9], 6, 1, 5}, {studentIDs[9], 6, 2, 5},
		{studentIDs[9], 12, 1, 5}, {studentIDs[9], 12, 2, 5},
		{studentIDs[10], 1, 1, 4}, {studentIDs[10], 1, 2, 4},
		{studentIDs[10], 3, 1, 4}, {studentIDs[10], 3, 2, 4},
		{studentIDs[10], 6, 1, 4}, {studentIDs[10], 6, 2, 4},
		{studentIDs[10], 12, 1, 4}, {studentIDs[10], 12, 2, 4},
		{studentIDs[11], 1, 1, 5}, {studentIDs[11], 1, 2, 5},
		{studentIDs[11], 3, 1, 4}, {studentIDs[11], 3, 2, 5},
		{studentIDs[11], 6, 1, 5}, {studentIDs[11], 6, 2, 5},
		{studentIDs[11], 12, 1, 5}, {studentIDs[11], 12, 2, 5},

		// 10A
		{studentIDs[12], 1, 1, 4}, {studentIDs[12], 1, 2, 5},
		{studentIDs[12], 3, 1, 5}, {studentIDs[12], 3, 2, 5},
		{studentIDs[12], 6, 1, 4}, {studentIDs[12], 6, 2, 5},
		{studentIDs[12], 12, 1, 5}, {studentIDs[12], 12, 2, 5},
		{studentIDs[13], 1, 1, 5}, {studentIDs[13], 1, 2, 5},
		{studentIDs[13], 3, 1, 5}, {studentIDs[13], 3, 2, 5},
		{studentIDs[13], 6, 1, 5}, {studentIDs[13], 6, 2, 5},
		{studentIDs[13], 12, 1, 5}, {studentIDs[13], 12, 2, 5},
		{studentIDs[14], 1, 1, 4}, {studentIDs[14], 1, 2, 4},
		{studentIDs[14], 3, 1, 4}, {studentIDs[14], 3, 2, 4},
		{studentIDs[14], 6, 1, 4}, {studentIDs[14], 6, 2, 4},
		{studentIDs[14], 12, 1, 4}, {studentIDs[14], 12, 2, 4},
		{studentIDs[15], 1, 1, 5}, {studentIDs[15], 1, 2, 5},
		{studentIDs[15], 3, 1, 5}, {studentIDs[15], 3, 2, 5},
		{studentIDs[15], 6, 1, 5}, {studentIDs[15], 6, 2, 5},
		{studentIDs[15], 12, 1, 5}, {studentIDs[15], 12, 2, 5},
		{studentIDs[16], 1, 1, 3}, {studentIDs[16], 1, 2, 4},
		{studentIDs[16], 3, 1, 3}, {studentIDs[16], 3, 2, 3},
		{studentIDs[16], 6, 1, 3}, {studentIDs[16], 6, 2, 4},
		{studentIDs[16], 12, 1, 3}, {studentIDs[16], 12, 2, 4},
		{studentIDs[17], 1, 1, 4}, {studentIDs[17], 1, 2, 4},
		{studentIDs[17], 3, 1, 4}, {studentIDs[17], 3, 2, 4},
		{studentIDs[17], 6, 1, 4}, {studentIDs[17], 6, 2, 4},
		{studentIDs[17], 12, 1, 4}, {studentIDs[17], 12, 2, 4},

		// 10B
		{studentIDs[18], 1, 1, 5}, {studentIDs[18], 1, 2, 5},
		{studentIDs[18], 3, 1, 4}, {studentIDs[18], 3, 2, 5},
		{studentIDs[18], 6, 1, 5}, {studentIDs[18], 6, 2, 5},
		{studentIDs[18], 12, 1, 5}, {studentIDs[18], 12, 2, 5},
		{studentIDs[19], 1, 1, 4}, {studentIDs[19], 1, 2, 4},
		{studentIDs[19], 3, 1, 4}, {studentIDs[19], 3, 2, 4},
		{studentIDs[19], 6, 1, 4}, {studentIDs[19], 6, 2, 4},
		{studentIDs[19], 12, 1, 4}, {studentIDs[19], 12, 2, 4},
		{studentIDs[20], 1, 1, 5}, {studentIDs[20], 1, 2, 5},
		{studentIDs[20], 3, 1, 5}, {studentIDs[20], 3, 2, 5},
		{studentIDs[20], 6, 1, 5}, {studentIDs[20], 6, 2, 5},
		{studentIDs[20], 12, 1, 5}, {studentIDs[20], 12, 2, 5},
		{studentIDs[21], 1, 1, 4}, {studentIDs[21], 1, 2, 4},
		{studentIDs[21], 3, 1, 4}, {studentIDs[21], 3, 2, 4},
		{studentIDs[21], 6, 1, 4}, {studentIDs[21], 6, 2, 4},
		{studentIDs[21], 12, 1, 4}, {studentIDs[21], 12, 2, 4},
		{studentIDs[22], 1, 1, 3}, {studentIDs[22], 1, 2, 4},
		{studentIDs[22], 3, 1, 3}, {studentIDs[22], 3, 2, 3},
		{studentIDs[22], 6, 1, 3}, {studentIDs[22], 6, 2, 4},
		{studentIDs[22], 12, 1, 3}, {studentIDs[22], 12, 2, 4},
		{studentIDs[23], 1, 1, 5}, {studentIDs[23], 1, 2, 5},
		{studentIDs[23], 3, 1, 5}, {studentIDs[23], 3, 2, 5},
		{studentIDs[23], 6, 1, 5}, {studentIDs[23], 6, 2, 5},
		{studentIDs[23], 12, 1, 5}, {studentIDs[23], 12, 2, 5},

		// 11A
		{studentIDs[24], 1, 1, 5}, {studentIDs[24], 1, 2, 5},
		{studentIDs[24], 3, 1, 5}, {studentIDs[24], 3, 2, 5},
		{studentIDs[24], 6, 1, 5}, {studentIDs[24], 6, 2, 5},
		{studentIDs[24], 12, 1, 5}, {studentIDs[24], 12, 2, 5},
		{studentIDs[25], 1, 1, 4}, {studentIDs[25], 1, 2, 4},
		{studentIDs[25], 3, 1, 4}, {studentIDs[25], 3, 2, 4},
		{studentIDs[25], 6, 1, 4}, {studentIDs[25], 6, 2, 4},
		{studentIDs[25], 12, 1, 4}, {studentIDs[25], 12, 2, 4},
		{studentIDs[26], 1, 1, 5}, {studentIDs[26], 1, 2, 5},
		{studentIDs[26], 3, 1, 5}, {studentIDs[26], 3, 2, 5},
		{studentIDs[26], 6, 1, 5}, {studentIDs[26], 6, 2, 5},
		{studentIDs[26], 12, 1, 5}, {studentIDs[26], 12, 2, 5},
		{studentIDs[27], 1, 1, 4}, {studentIDs[27], 1, 2, 4},
		{studentIDs[27], 3, 1, 4}, {studentIDs[27], 3, 2, 4},
		{studentIDs[27], 6, 1, 4}, {studentIDs[27], 6, 2, 4},
		{studentIDs[27], 12, 1, 4}, {studentIDs[27], 12, 2, 4},
		{studentIDs[28], 1, 1, 5}, {studentIDs[28], 1, 2, 5},
		{studentIDs[28], 3, 1, 5}, {studentIDs[28], 3, 2, 5},
		{studentIDs[28], 6, 1, 5}, {studentIDs[28], 6, 2, 5},
		{studentIDs[28], 12, 1, 5}, {studentIDs[28], 12, 2, 5},
		{studentIDs[29], 1, 1, 4}, {studentIDs[29], 1, 2, 4},
		{studentIDs[29], 3, 1, 4}, {studentIDs[29], 3, 2, 4},
		{studentIDs[29], 6, 1, 4}, {studentIDs[29], 6, 2, 4},
		{studentIDs[29], 12, 1, 4}, {studentIDs[29], 12, 2, 4},
	}

	for _, g := range grades {
		_, err := db.Exec(`
			INSERT INTO grades (student_id, subject_id, grading_period_id, grade)
			VALUES ($1, $2, $3, $4)
			ON CONFLICT DO NOTHING
		`, g.studentID, g.subjectID, g.gradingPeriodID, g.grade)
		if err != nil {
			return fmt.Errorf("failed to seed grades: %w", err)
		}
	}

	// Пользователи для входа
	passwordHash, err := bcrypt.GenerateFromPassword([]byte("password123"), bcrypt.DefaultCost)
	if err != nil {
		return fmt.Errorf("failed to hash password: %w", err)
	}

	users := []struct {
		username  string
		email     string
		password  string
		role      string
		teacherID *int
	}{
		{"admin", "admin@school.ru", string(passwordHash), "admin", nil},
		{"teacher1", "teacher1@school.ru", string(passwordHash), "teacher", &teacherIDs[0]},
		{"teacher2", "teacher2@school.ru", string(passwordHash), "teacher", &teacherIDs[1]},
		{"headteacher", "headteacher@school.ru", string(passwordHash), "head_teacher", &teacherIDs[0]},
	}

	for _, u := range users {
		_, err := db.Exec(`
			INSERT INTO auth_users (username, email, password_hash, role, teacher_id)
			VALUES ($1, $2, $3, $4, $5)
			ON CONFLICT (username) DO NOTHING
		`, u.username, u.email, u.password, u.role, u.teacherID)
		if err != nil {
			return fmt.Errorf("failed to seed auth_users: %w", err)
		}
	}

	log.Println("Main data seeded successfully")
	return nil
}

func strPtr(s string) *string {
	return &s
}

func intPtr(i int) *int {
	return &i
}
