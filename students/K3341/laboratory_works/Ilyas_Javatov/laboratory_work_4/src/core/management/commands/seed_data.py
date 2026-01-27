from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import (
    Classroom,
    Grade,
    Schedule,
    SchoolClass,
    Student,
    Subject,
    Teacher,
    TeachingAssignment,
)


class Command(BaseCommand):
    help = "Заполняет базу тестовыми данными для школьной системы"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Создание тестовых данных...")

        subjects = [
            "Математика",
            "Русский язык",
            "Литература",
            "История",
            "Физика",
            "Химия",
            "Биология",
            "Информатика",
            "Английский язык",
        ]
        subject_map = {}
        for name in subjects:
            subject_map[name], _ = Subject.objects.get_or_create(name=name)

        classrooms = [
            ("101", "base"),
            ("102", "base"),
            ("201", "profile"),
            ("202", "profile"),
            ("303", "base"),
        ]
        classroom_map = {}
        for room_number, subject_type in classrooms:
            classroom_map[room_number], _ = Classroom.objects.get_or_create(
                room_number=room_number,
                defaults={"subject_type": subject_type},
            )

        teachers_data = [
            ("ivanov", "Иван", "Иванов", "101", ["Математика", "Физика"]),
            ("petrova", "Анна", "Петрова", "102", ["Русский язык", "Литература"]),
            ("sidorov", "Петр", "Сидоров", None, ["Информатика"]),
            ("smirnova", "Елена", "Смирнова", "201", ["Химия", "Биология"]),
            ("volkov", "Олег", "Волков", "202", ["История", "Английский язык"]),
        ]
        teacher_map = {}
        for username, first_name, last_name, room, subject_names in teachers_data:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@school.local",
                    "first_name": first_name,
                    "last_name": last_name,
                },
            )
            if not user.has_usable_password():
                user.set_password("pass1234")
                user.save()
            classroom = classroom_map.get(room) if room else None
            teacher, _ = Teacher.objects.get_or_create(
                user=user,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "classroom": classroom,
                },
            )
            teacher.classroom = classroom
            teacher.first_name = first_name
            teacher.last_name = last_name
            teacher.save()
            teacher.subjects.set([subject_map[name] for name in subject_names])
            teacher_map[username] = teacher

        classes = ["7А", "7Б", "8А"]
        class_map = {}
        for class_name in classes:
            class_map[class_name], _ = SchoolClass.objects.get_or_create(
                name=class_name
            )

        class_map["7А"].class_teacher = teacher_map["ivanov"]
        class_map["7А"].save()
        class_map["7Б"].class_teacher = teacher_map["petrova"]
        class_map["7Б"].save()
        class_map["8А"].class_teacher = teacher_map["sidorov"]
        class_map["8А"].save()

        students_data = [
            ("Илья", "Кузнецов", "M", "7А"),
            ("Мария", "Ильина", "F", "7А"),
            ("Артем", "Морозов", "M", "7А"),
            ("Ольга", "Калинина", "F", "7Б"),
            ("Егор", "Зайцев", "M", "7Б"),
            ("Алина", "Соколова", "F", "7Б"),
            ("Дмитрий", "Котов", "M", "8А"),
            ("Екатерина", "Орлова", "F", "8А"),
        ]
        student_map = {}
        for first_name, last_name, gender, class_name in students_data:
            student, _ = Student.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                school_class=class_map[class_name],
                defaults={"gender": gender},
            )
            student.gender = gender
            student.school_class = class_map[class_name]
            student.save()
            student_map[f"{last_name} {first_name}"] = student

        assignments = [
            ("ivanov", "Математика", "7А"),
            ("ivanov", "Физика", "8А"),
            ("petrova", "Русский язык", "7А"),
            ("petrova", "Литература", "7Б"),
            ("sidorov", "Информатика", "7А"),
            ("sidorov", "Информатика", "8А"),
            ("smirnova", "Химия", "8А"),
            ("smirnova", "Биология", "7Б"),
            ("volkov", "История", "7Б"),
            ("volkov", "Английский язык", "7А"),
        ]
        for teacher_key, subject_name, class_name in assignments:
            TeachingAssignment.objects.get_or_create(
                teacher=teacher_map[teacher_key],
                subject=subject_map[subject_name],
                school_class=class_map[class_name],
                defaults={"start_date": "2025-09-01"},
            )

        schedule_items = [
            ("7А", "Математика", "ivanov", 1, 1),
            ("7А", "Русский язык", "petrova", 1, 2),
            ("7А", "Информатика", "sidorov", 1, 3),
            ("7А", "Английский язык", "volkov", 2, 1),
            ("7А", "Литература", "petrova", 2, 2),
            ("7Б", "Литература", "petrova", 1, 1),
            ("7Б", "Биология", "smirnova", 1, 2),
            ("7Б", "История", "volkov", 2, 1),
            ("8А", "Физика", "ivanov", 1, 1),
            ("8А", "Информатика", "sidorov", 1, 2),
            ("8А", "Химия", "smirnova", 2, 1),
        ]
        for class_name, subject_name, teacher_key, day, lesson in schedule_items:
            Schedule.objects.get_or_create(
                school_class=class_map[class_name],
                subject=subject_map[subject_name],
                teacher=teacher_map[teacher_key],
                day_of_week=day,
                lesson_number=lesson,
            )

        grades_data = [
            ("Кузнецов Илья", "Математика", 5, 1),
            ("Кузнецов Илья", "Информатика", 4, 1),
            ("Ильина Мария", "Математика", 4, 1),
            ("Ильина Мария", "Русский язык", 5, 1),
            ("Морозов Артем", "Математика", 3, 1),
            ("Калинина Ольга", "Литература", 5, 1),
            ("Калинина Ольга", "История", 4, 1),
            ("Зайцев Егор", "Биология", 4, 1),
            ("Соколова Алина", "Литература", 5, 1),
            ("Котов Дмитрий", "Физика", 4, 1),
            ("Орлова Екатерина", "Информатика", 5, 1),
        ]
        for student_key, subject_name, grade_value, quarter in grades_data:
            Grade.objects.get_or_create(
                student=student_map[student_key],
                subject=subject_map[subject_name],
                quarter=quarter,
                school_year="2025-2026",
                defaults={"grade": grade_value},
            )

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно добавлены."))
