from django.db.models import Count
from django.http import FileResponse, Http404
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from school import models, serializers, services


class AuthenticatedModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]


class TeacherViewSet(AuthenticatedModelViewSet):
    queryset = models.Teacher.objects.all().prefetch_related("subjects", "assigned_room")
    serializer_class = serializers.TeacherSerializer
    filterset_fields = ("subjects", "assigned_room")
    search_fields = ("last_name", "first_name", "middle_name", "email")
    ordering_fields = ("last_name", "hired_at")


class StudentViewSet(AuthenticatedModelViewSet):
    queryset = models.Student.objects.all().select_related("school_class")
    serializer_class = serializers.StudentSerializer
    filterset_fields = ("school_class", "gender", "is_active")
    search_fields = ("last_name", "first_name", "middle_name")
    ordering_fields = ("last_name", "created_at")


class SchoolClassViewSet(AuthenticatedModelViewSet):
    queryset = models.SchoolClass.objects.all().select_related("homeroom_teacher")
    serializer_class = serializers.SchoolClassSerializer
    filterset_fields = ("grade_level", "profile")
    search_fields = ("title",)
    ordering_fields = ("grade_level", "title")


class SubjectViewSet(AuthenticatedModelViewSet):
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
    filterset_fields = ("category",)
    search_fields = ("name", "code")
    ordering_fields = ("name", "code")


class ClassroomViewSet(AuthenticatedModelViewSet):
    queryset = models.Classroom.objects.all()
    serializer_class = serializers.ClassroomSerializer
    filterset_fields = ("category",)
    ordering_fields = ("number", "capacity")
    search_fields = ("number", "title")


class TeacherSubjectViewSet(AuthenticatedModelViewSet):
    queryset = models.TeacherSubject.objects.select_related("teacher", "subject").all()
    serializer_class = serializers.TeacherSubjectSerializer
    filterset_fields = ("teacher", "subject")


class TeachingAssignmentViewSet(AuthenticatedModelViewSet):
    queryset = (
        models.TeachingAssignment.objects.select_related(
            "teacher", "subject", "school_class"
        ).all()
    )
    serializer_class = serializers.TeachingAssignmentSerializer
    filterset_fields = ("teacher", "subject", "school_class")


class GradeViewSet(AuthenticatedModelViewSet):
    queryset = models.Grade.objects.select_related(
        "student", "subject", "graded_by"
    ).all()
    serializer_class = serializers.GradeSerializer
    filterset_fields = ("subject", "quarter", "student__school_class")
    ordering_fields = ("quarter", "value")


class ScheduleEntryViewSet(AuthenticatedModelViewSet):
    queryset = models.ScheduleEntry.objects.select_related(
        "school_class", "subject", "teacher", "room"
    ).all()
    serializer_class = serializers.ScheduleEntrySerializer
    filterset_fields = ("school_class", "weekday", "teacher")
    ordering_fields = ("weekday", "lesson_number")


class ScheduleLookupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = serializers.ScheduleLookupSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            entry = models.ScheduleEntry.objects.select_related(
                "school_class", "subject", "teacher", "room"
            ).get(
                school_class=data["school_class"],
                weekday=data["weekday"],
                lesson_number=data["lesson_number"],
            )
        except models.ScheduleEntry.DoesNotExist as exc:
            raise Http404 from exc
        return Response(serializers.ScheduleEntrySerializer(entry).data)


class SubjectTeacherCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        subjects = (
            models.Subject.objects.annotate(
                teachers_count=Count("teachers", distinct=True)
            )
            .values("id", "code", "name", "teachers_count")
            .order_by("name")
        )
        return Response(list(subjects))


class SubjectPeersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, class_id: int):
        payload = {"class_id": class_id, **request.query_params}
        serializer = serializers.SubjectPeersQuerySerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        school_class = serializer.validated_data["school_class"]
        subject_code = serializer.validated_data.get("subject_code") or "INF"
        subject = (
            models.Subject.objects.filter(code__iexact=subject_code).first()
            or models.Subject.objects.filter(name__icontains="информат").first()
        )
        if not subject:
            raise Http404("Предмет не найден")

        assignments = models.TeachingAssignment.objects.filter(
            school_class=school_class, subject=subject
        ).select_related("teacher")
        if not assignments.exists():
            raise Http404("Для класса нет преподавателя по предмету")

        teacher_ids = list(assignments.values_list("teacher_id", flat=True))
        related_subjects = list(
            models.Teacher.objects.filter(id__in=teacher_ids)
            .values_list("subjects__id", flat=True)
            .distinct()
        )
        if not related_subjects:
            return Response([])
        peers = (
            models.Teacher.objects.filter(subjects__in=related_subjects)
            .exclude(id__in=teacher_ids)
            .distinct()
            .prefetch_related("subjects", "assigned_room")
        )

        return Response(serializers.TeacherSerializer(peers, many=True).data)


class GenderDistributionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stats = (
            models.Student.objects.values("school_class__id", "school_class__title", "gender")
            .annotate(total=Count("id"))
            .order_by("school_class__grade_level", "school_class__title")
        )
        result = {}
        for entry in stats:
            class_id = entry["school_class__id"]
            if class_id not in result:
                result[class_id] = {
                    "class_id": class_id,
                    "class_title": entry["school_class__title"],
                    "boys": 0,
                    "girls": 0,
                }
            if entry["gender"] == models.Gender.MALE:
                result[class_id]["boys"] = entry["total"]
            else:
                result[class_id]["girls"] = entry["total"]
        return Response(list(result.values()))


class ClassroomCategoryStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stats = (
            models.Classroom.objects.values("category")
            .annotate(total=Count("id"))
            .order_by("category")
        )
        return Response(list(stats))


class ClassPerformanceReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, class_id: int):
        serializer = serializers.ClassReportRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        try:
            service = services.ClassPerformanceReportService(
                school_class_id=class_id,
                quarter=serializer.validated_data.get("quarter"),
            )
        except models.SchoolClass.DoesNotExist as exc:
            raise Http404 from exc
        return Response(service.as_dict())


class ClassPerformanceReportDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, class_id: int):
        serializer = serializers.ClassReportRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        try:
            service = services.ClassPerformanceReportService(
                school_class_id=class_id,
                quarter=serializer.validated_data.get("quarter"),
            )
        except models.SchoolClass.DoesNotExist as exc:
            raise Http404 from exc
        buffer = service.as_pdf()
        filename = f"class-report-{class_id}.pdf"
        return FileResponse(
            buffer,
            as_attachment=True,
            filename=filename,
            content_type="application/pdf",
        )
