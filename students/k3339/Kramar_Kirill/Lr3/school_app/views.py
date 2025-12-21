from django.db import IntegrityError
from rest_framework import status
from rest_framework import generics, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Avg
from .models import Teacher, Student, QuarterGrade, Lesson, Classroom, Subject, Klass
from .serializers import TeacherSerializer, StudentSerializer, QuarterGradeSerializer, LessonSerializer, \
    SubjectSerializer, ClassroomSerializer, KlassSerializer, LessonCreateUpdateSerializer, \
    TeacherCreateUpdateSerializer, StudentCreateUpdateSerializer, QuarterGradeCreateUpdateSerializer, \
    ClassroomCreateUpdateSerializer, SubjectCreateUpdateSerializer, KlassCreateUpdateSerializer


class BaseEntityViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return self.create_update_serializer_class or self.serializer_class
        return self.serializer_class

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:  # Retrieve specific entity
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)  # List all entities

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class TeachersViewSet(BaseEntityViewSet):
    model = Teacher
    serializer_class = TeacherSerializer
    create_update_serializer_class = TeacherCreateUpdateSerializer


class StudentsViewSet(BaseEntityViewSet):
    model = Student
    serializer_class = StudentSerializer
    create_update_serializer_class = StudentCreateUpdateSerializer


class QuarterGradesViewSet(BaseEntityViewSet):
    model = QuarterGrade
    serializer_class = QuarterGradeSerializer
    create_update_serializer_class = QuarterGradeCreateUpdateSerializer


class LessonsViewSet(BaseEntityViewSet):
    model = Lesson
    serializer_class = LessonSerializer
    create_update_serializer_class = LessonCreateUpdateSerializer

class ClassroomsViewSet(BaseEntityViewSet):
    model = Classroom
    serializer_class = ClassroomSerializer
    create_update_serializer_class = ClassroomCreateUpdateSerializer


class SubjectsViewSet(BaseEntityViewSet):
    model = Subject
    serializer_class = SubjectSerializer
    create_update_serializer_class = SubjectCreateUpdateSerializer


class KlassViewSet(BaseEntityViewSet):
    model = Klass
    serializer_class = KlassSerializer
    create_update_serializer_class = KlassCreateUpdateSerializer

class SubjectInClassAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, klass_id, weekday, lesson_number):
        try:
            lesson = Lesson.objects.get(klass_id=klass_id, weekday=weekday, lesson_number=lesson_number)
            subject_name = lesson.subject.name
            return Response({"Subject": subject_name})
        except Lesson.DoesNotExist:
            return Response({"Error": "Lesson not found."}, status=404)


class TeachersPerSubjectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teachers_count = Teacher.objects.values('subject__name').annotate(count=Count('id'))
        data = {entry['subject__name']: entry['count'] for entry in teachers_count}
        return Response({"TeachersPerSubject": data})


class TeachersWithSameSubjectsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, klass_id):
        try:
            informatics_teacher = Teacher.objects.filter(
                subject__name="Informatics",
                klass__id=klass_id
            ).first()

            if not informatics_teacher:
                return Response({"Error": "Informatics teacher not found in the specified class."}, status=404)

            teachers = Teacher.objects.filter(subject__in=informatics_teacher.subject.all()).exclude(id=informatics_teacher.id)
            serializer = TeacherSerializer(teachers, many=True)
            return Response({"TeachersWithSameSubjects": serializer.data})
        except Exception as e:
            return Response({"Error": str(e)}, status=500)


class GenderCountInClassesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        classes = Klass.objects.all()
        data = {}
        for klass in classes:
            boys = Student.objects.filter(klass=klass, gender="Male").count()
            girls = Student.objects.filter(klass=klass, gender="Female").count()
            data[klass.id] = {"boys": boys, "girls": girls}
        return Response({"GenderCounts": data})


class ClassroomCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        classrooms = Classroom.objects.values('type').annotate(count=Count('id'))
        data = {entry['type']: entry['count'] for entry in classrooms}
        return Response({"ClassroomCounts": data})


class ClassPerformanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, klass_id):
        try:
            students = Student.objects.filter(klass__id=klass_id)
            grades = QuarterGrade.objects.filter(student__klass__id=klass_id)
            subjects = Subject.objects.all()
            report = {}

            for subject in subjects:
                subject_grades = grades.filter(subject=subject)
                if subject_grades.exists():
                    avg_grade = subject_grades.aggregate(avg=Avg('grade'))['avg']
                    report[subject.name] = {"average_grade": avg_grade, "grades": list(subject_grades.values())}

            class_teacher = Klass.objects.get(id=klass_id).class_teacher
            return Response({
                "class_teacher": f"{class_teacher.first_name} {class_teacher.last_name}" if class_teacher else None,
                "total_students": students.count(),
                "report": report
            })
        except Klass.DoesNotExist:
            return Response({"Error": "Class not found."}, status=404)

class StudentsInClassAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, klass_id):
        try:
            students = Student.objects.filter(klass__id=klass_id)
            serializer = StudentSerializer(students, many=True)
            return Response({"Students": serializer.data}, status=200)
        except Exception as e:
            return Response({"Error": str(e)}, status=500)