from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from school import models, services


class BaseAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(username="test", password="testpass")
        cls.token = Token.objects.create(user=cls.user)

        cls.classroom = models.Classroom.objects.create(number="101", category=models.RoomCategory.BASIC)
        cls.subject = models.Subject.objects.create(code="MATH", name="Математика")
        cls.school_class = models.SchoolClass.objects.create(
            title="10А",
            grade_level=10,
            profile=models.SubjectCategory.BASIC,
        )
        cls.teacher = models.Teacher.objects.create(
            first_name="Анна",
            last_name="Иванова",
            assigned_room=cls.classroom,
        )
        cls.teacher.subjects.add(cls.subject)
        cls.school_class.homeroom_teacher = cls.teacher
        cls.school_class.save()

        cls.assignment = models.TeachingAssignment.objects.create(
            teacher=cls.teacher,
            subject=cls.subject,
            school_class=cls.school_class,
        )

        cls.student = models.Student.objects.create(
            first_name="Пётр",
            last_name="Сидоров",
            gender=models.Gender.MALE,
            school_class=cls.school_class,
        )

        cls.grade = models.Grade.objects.create(
            student=cls.student,
            subject=cls.subject,
            quarter=models.Quarter.Q1,
            value=5,
            graded_by=cls.teacher,
        )

        cls.schedule = models.ScheduleEntry.objects.create(
            school_class=cls.school_class,
            subject=cls.subject,
            teacher=cls.teacher,
            room=cls.classroom,
            weekday=models.WeekDay.MONDAY,
            lesson_number=1,
        )

    def auth_headers(self):
        return {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}


class ScheduleLookupTests(BaseAPITestCase):
    def test_schedule_lookup_returns_entry(self):
        response = self.client.get(
            "/api/analytics/schedule/lookup/",
            {
                "class_id": self.school_class.id,
                "weekday": models.WeekDay.MONDAY,
                "lesson_number": 1,
            },
            **self.auth_headers(),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["subject"], self.subject.id)
        self.assertEqual(response.data["teacher"], self.teacher.id)


class ReportServiceTests(BaseAPITestCase):
    def test_report_payload_contains_class_average(self):
        service = services.ClassPerformanceReportService(
            school_class_id=self.school_class.id,
            quarter=models.Quarter.Q1,
        )
        data = service.as_dict()
        self.assertEqual(data["class_average"], 5)
        self.assertEqual(data["students_total"], 1)
        self.assertEqual(len(data["subjects"]), 1)

    def test_report_pdf_generation(self):
        service = services.ClassPerformanceReportService(
            school_class_id=self.school_class.id,
            quarter=models.Quarter.Q1,
        )
        pdf_buffer = service.as_pdf()
        self.assertGreater(len(pdf_buffer.getvalue()), 0)

