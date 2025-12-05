from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from statistics import mean
from typing import Dict, List, Optional

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from school import models


@dataclass
class SubjectReportItem:
    subject_id: int
    subject_name: str
    grades: List[Dict]

    @property
    def average(self) -> Optional[float]:
        values = [grade["value"] for grade in self.grades]
        return round(mean(values), 2) if values else None


class ClassPerformanceReportService:
    """Сервис подготовки отчета об успеваемости класса."""

    def __init__(self, school_class_id: int, quarter: Optional[int] = None):
        self.school_class = models.SchoolClass.objects.select_related(
            "homeroom_teacher"
        ).get(pk=school_class_id)
        self.quarter = quarter

    def _grades_queryset(self):
        qs = models.Grade.objects.filter(student__school_class=self.school_class)
        if self.quarter:
            qs = qs.filter(quarter=self.quarter)
        return qs.select_related("student", "subject").order_by("subject__name")

    def as_dict(self) -> Dict:
        grades = list(self._grades_queryset())
        subject_map: Dict[int, SubjectReportItem] = {}
        all_values: List[int] = []

        for grade in grades:
            subject_id = grade.subject_id
            if subject_id not in subject_map:
                subject_map[subject_id] = SubjectReportItem(
                    subject_id=subject_id,
                    subject_name=grade.subject.name,
                    grades=[],
                )
            grade_payload = {
                "student_id": grade.student_id,
                "student_name": grade.student.full_name,
                "value": grade.value,
                "quarter": grade.quarter,
            }
            subject_map[subject_id].grades.append(grade_payload)
            all_values.append(grade.value)

        subjects_payload = [
            {
                "subject_id": item.subject_id,
                "subject_name": item.subject_name,
                "average_grade": item.average,
                "grades": item.grades,
            }
            for item in subject_map.values()
        ]

        class_average = round(mean(all_values), 2) if all_values else None

        homeroom_teacher = self.school_class.homeroom_teacher
        homeroom_payload = (
            {
                "id": homeroom_teacher.id,
                "full_name": homeroom_teacher.full_name,
            }
            if homeroom_teacher
            else None
        )

        return {
            "class_id": self.school_class.id,
            "class_title": self.school_class.title,
            "quarter": self.quarter,
            "students_total": self.school_class.students.count(),
            "homeroom_teacher": homeroom_payload,
            "subjects": subjects_payload,
            "class_average": class_average,
        }

    def as_pdf(self) -> BytesIO:
        """Сформировать PDF-отчет."""
        payload = self.as_dict()
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        pdf.setTitle(f"Отчет по классу {payload['class_title']}")
        y = height - 40
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(40, y, f"Отчет по классу {payload['class_title']}")
        y -= 24
        pdf.setFont("Helvetica", 12)
        pdf.drawString(40, y, f"Четверть: {payload['quarter'] or 'Все'}")
        y -= 18
        pdf.drawString(40, y, f"Всего учеников: {payload['students_total']}")
        y -= 18
        pdf.drawString(
            40,
            y,
            f"Классный руководитель: {payload['homeroom_teacher']['full_name'] if payload['homeroom_teacher'] else 'не назначен'}",
        )
        y -= 24
        pdf.drawString(
            40,
            y,
            f"Средний балл класса: {payload['class_average'] or 'n/a'}",
        )
        y -= 30

        for subject in payload["subjects"]:
            if y < 120:
                pdf.showPage()
                y = height - 40
                pdf.setFont("Helvetica", 12)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(
                40,
                y,
                f"{subject['subject_name']} (ср. балл: {subject['average_grade'] or 'n/a'})",
            )
            y -= 18
            pdf.setFont("Helvetica", 11)
            for grade in subject["grades"]:
                pdf.drawString(
                    60,
                    y,
                    f"{grade['student_name']}: {grade['value']} (четверть {grade['quarter']})",
                )
                y -= 16
                if y < 80:
                    pdf.showPage()
                    y = height - 40
                    pdf.setFont("Helvetica", 11)

        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        return buffer

