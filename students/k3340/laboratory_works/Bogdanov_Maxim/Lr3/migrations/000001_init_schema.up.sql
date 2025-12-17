-- Справочник: учебные годы
CREATE TABLE academic_years
(
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(9)  NOT NULL UNIQUE, -- например "2024-2025"
    start_date DATE        NOT NULL,
    end_date   DATE        NOT NULL,
    is_current BOOLEAN     NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (start_date < end_date)
);

-- Справочник: типы дисциплин
CREATE TABLE subject_types
(
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Справочник: предметы
CREATE TABLE subjects
(
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL UNIQUE,
    subject_type_id INTEGER      NOT NULL REFERENCES subject_types (id),
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Справочник: пол
CREATE TABLE genders
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE
);

-- Справочник: дни недели
CREATE TABLE weekdays
(
    id        SERIAL PRIMARY KEY,
    name      VARCHAR(20) NOT NULL UNIQUE,
    day_order INTEGER     NOT NULL UNIQUE CHECK (day_order BETWEEN 1 AND 7)
);

-- Справочник: оценочные периоды (четверти)
CREATE TABLE grading_periods
(
    id               SERIAL PRIMARY KEY,
    academic_year_id INTEGER     NOT NULL REFERENCES academic_years (id),
    name             VARCHAR(50) NOT NULL, -- "1 четверть", "2 четверть" и т.д.
    period_order     INTEGER     NOT NULL CHECK (period_order BETWEEN 1 AND 4),
    start_date       DATE        NOT NULL,
    end_date         DATE        NOT NULL,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (academic_year_id, period_order),
    CHECK (start_date < end_date)
);

-- Кабинеты
CREATE TABLE classrooms
(
    id              SERIAL PRIMARY KEY,
    room_number     VARCHAR(10) NOT NULL UNIQUE,
    subject_type_id INTEGER     NOT NULL REFERENCES subject_types (id),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Учителя
CREATE TABLE teachers
(
    id           SERIAL PRIMARY KEY,
    first_name   VARCHAR(50) NOT NULL,
    last_name    VARCHAR(50) NOT NULL,
    middle_name  VARCHAR(50),
    classroom_id INTEGER REFERENCES classrooms (id), -- закрепленный кабинет (может быть общий)
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at   TIMESTAMPTZ                         
);

-- Связь учителей и предметов (многие-ко-многим)
CREATE TABLE teacher_subjects
(
    id         SERIAL PRIMARY KEY,
    teacher_id INTEGER     NOT NULL REFERENCES teachers (id),
    subject_id INTEGER     NOT NULL REFERENCES subjects (id),
    start_date DATE        NOT NULL,
    end_date   DATE, -- NULL если преподает в настоящее время
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (teacher_id, subject_id, start_date)
);

-- Классы
CREATE TABLE classes
(
    id               SERIAL PRIMARY KEY,
    grade            INTEGER     NOT NULL CHECK (grade BETWEEN 1 AND 11),
    letter           VARCHAR(5)  NOT NULL,
    academic_year_id INTEGER     NOT NULL REFERENCES academic_years (id),
    class_teacher_id INTEGER REFERENCES teachers (id),
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at       TIMESTAMPTZ,                     
    UNIQUE (grade, letter, academic_year_id)
);

-- Ученики
CREATE TABLE students
(
    id          SERIAL PRIMARY KEY,
    first_name  VARCHAR(50) NOT NULL,
    last_name   VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    gender_id   INTEGER     NOT NULL REFERENCES genders (id),
    class_id    INTEGER     NOT NULL REFERENCES classes (id),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at  TIMESTAMPTZ
);

-- Расписание занятий
CREATE TABLE schedule
(
    id            SERIAL PRIMARY KEY,
    class_id      INTEGER     NOT NULL REFERENCES classes (id),
    weekday_id    INTEGER     NOT NULL REFERENCES weekdays (id),
    lesson_number INTEGER     NOT NULL CHECK (lesson_number BETWEEN 1 AND 10),
    subject_id    INTEGER     NOT NULL REFERENCES subjects (id),
    teacher_id    INTEGER     NOT NULL REFERENCES teachers (id),
    classroom_id  INTEGER     NOT NULL REFERENCES classrooms (id),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (class_id, weekday_id, lesson_number)
);

-- Оценки
CREATE TABLE grades
(
    id                SERIAL PRIMARY KEY,
    student_id        INTEGER     NOT NULL REFERENCES students (id),
    subject_id        INTEGER     NOT NULL REFERENCES subjects (id),
    grading_period_id INTEGER     NOT NULL REFERENCES grading_periods (id),
    grade             INTEGER     NOT NULL CHECK (grade BETWEEN 1 AND 5),
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (student_id, subject_id, grading_period_id)
);

CREATE TABLE auth_users
(
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(50) NOT NULL UNIQUE,
    email         VARCHAR(255) UNIQUE,
    password_hash TEXT        NOT NULL,
    role          VARCHAR(30) NOT NULL,             -- 'admin', 'head_teacher', 'teacher' и т.п.
    teacher_id    INTEGER REFERENCES teachers (id), -- Связь с учителем (если это учетная запись учителя)
    is_active     BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at    TIMESTAMPTZ
);

CREATE TABLE auth_refresh_tokens
(
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER   NOT NULL REFERENCES auth_users (id) ON DELETE CASCADE,
    token_hash TEXT      NOT NULL,
    issued_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (token_hash)
);

-- Индексы для учителей
CREATE INDEX idx_teachers_classroom ON teachers (classroom_id) WHERE deleted_at IS NULL AND classroom_id IS NOT NULL;

-- Индексы для учеников
CREATE INDEX idx_students_class ON students (class_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_students_class_gender ON students (class_id, gender_id) WHERE deleted_at IS NULL;

-- Индексы для классов
CREATE INDEX idx_classes_academic_year ON classes (academic_year_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_classes_teacher ON classes (class_teacher_id) WHERE deleted_at IS NULL AND class_teacher_id IS NOT NULL;

-- Индексы для расписания (основной запрос: класс + день + урок)
CREATE INDEX idx_schedule_class_weekday_lesson ON schedule (class_id, weekday_id, lesson_number);
CREATE INDEX idx_schedule_teacher ON schedule (teacher_id);
CREATE INDEX idx_schedule_subject ON schedule (subject_id);
CREATE INDEX idx_schedule_classroom ON schedule (classroom_id);

-- Индексы для оценок (отчеты по успеваемости)
CREATE INDEX idx_grades_student_period ON grades (student_id, grading_period_id);
CREATE INDEX idx_grades_period_subject ON grades (grading_period_id, subject_id);

-- Индексы для связи учителей и предметов
CREATE INDEX idx_teacher_subjects_teacher ON teacher_subjects (teacher_id) WHERE end_date IS NULL;
CREATE INDEX idx_teacher_subjects_subject ON teacher_subjects (subject_id) WHERE end_date IS NULL;

-- Индексы для оценочных периодов
CREATE INDEX idx_grading_periods_academic_year ON grading_periods (academic_year_id);

-- Индекс для текущего учебного года
CREATE UNIQUE INDEX idx_academic_years_current ON academic_years (is_current) WHERE is_current = TRUE;

-- Индексы для справочников (FK)
CREATE INDEX idx_subjects_type ON subjects (subject_type_id);
CREATE INDEX idx_classrooms_type ON classrooms (subject_type_id);

CREATE INDEX idx_auth_users_active_username ON auth_users(username) WHERE deleted_at IS NULL AND is_active = TRUE;

CREATE INDEX idx_auth_users_role_active ON auth_users(role) WHERE deleted_at IS NULL AND is_active = TRUE;

CREATE INDEX idx_auth_users_teacher_active ON auth_users(teacher_id) WHERE deleted_at IS NULL AND is_active = TRUE;

CREATE INDEX idx_auth_refresh_tokens_user_active ON auth_refresh_tokens(user_id) WHERE revoked_at IS NULL;
CREATE INDEX idx_auth_refresh_tokens_expires_at ON auth_refresh_tokens(expires_at);