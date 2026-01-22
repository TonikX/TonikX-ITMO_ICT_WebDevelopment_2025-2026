from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} ({self.role})"


class Subject(models.Model):
    name = models.CharField(max_length=50)

    def get_subject_teachers(self):
        """Returns all teachers in this subject."""
        return self.teachers.all()

    def get_classes_with_subject(self):
        """Returns all classes in this subject."""
        return self.class_subjects.all()

    def get_homeworks_for_class(self, school_class):
        """Returns homeworks for this subject in specific class."""
        return self.homeworks.filter(school_class=school_class)

    def get_active_homeworks(self):
        """Returns active (not overdue) homeworks for this subject."""
        return self.homeworks.filter(due_date__gte=timezone.now().date())

    def __str__(self):
        return self.name


class SchoolClass(models.Model):
    name = models.CharField(max_length=20, unique=True)
    class_number = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Class number must be at least 1"),
            MaxValueValidator(11, message="Class number cannot exceed 11")
        ]
    )
    subjects = models.ManyToManyField(
        Subject,
        related_name='class_subjects',
        blank=True
    )

    def get_all_students(self):
        """Returns all students in this class."""
        return self.students.all()

    def get_all_subjects(self):
        """Returns all subjects in this class."""
        return self.subjects.all()

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField()
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.school_class})"

    def get_all_subjects(self):
        """Returns all subjects in this class."""
        return self.school_class.subjects.all()

    def get_subject_homeworks(self, subject):
        """Returns all homeworks for specific subject."""
        return Homework.objects.filter(subject=subject, school_class=self.school_class)

    def get_subject_grades(self, subject):
        """Returns all grades for this subject."""
        submissions = HomeworkSubmission.objects.filter(
            student=self,
            homework__subject=subject
        ).exclude(grade__isnull=True)
        return [submission.grade for submission in submissions]

    def get_average_grade(self, subject=None):
        """Returns average grade (optional) for this subject."""
        submissions = HomeworkSubmission.objects.filter(student=self).exclude(grade__isnull=True)

        if subject:
            submissions = submissions.filter(homework__subject=subject)

        if submissions.exists():
            avg =  submissions.aggregate(models.Avg('grade'))['grade__avg']
            return round(avg, 2) if avg is not None else None
        return None

    def get_submitted_homeworks(self):
        """Returns all submitted homeworks."""
        return self.submissions.all()

    def get_unsubmitted_homeworks(self):
        """Returns all unsubmitted homeworks."""
        class_homeworks = Homework.objects.filter(school_class=self.school_class)
        submitted_homework_ids = self.submissions.values_list('homework_id', flat=True)
        return class_homeworks.exclude(id__in=submitted_homework_ids)

    def get_pending_homeworks(self):
        """Returns all pending homeworks."""
        unsubmitted = self.get_unsubmitted_homeworks()
        return unsubmitted.filter(due_date__gt=timezone.now().date())

    def get_overdue_homeworks(self):
        """Returns all overdue homeworks."""
        unsubmitted = self.get_unsubmitted_homeworks()
        return unsubmitted.filter(due_date__lte=timezone.now().date())

    def get_burning_homeworks(self):
        """Returns all burning homeworks (due within a week)."""
        unsubmitted = self.get_unsubmitted_homeworks()
        today = timezone.now().date()
        week_later = today + timedelta(days=7)
        return unsubmitted.filter(due_date__range=(today, week_later))

    def get_homework_status(self, homework):
        """Returns homework status for this homework."""
        try:
            submission = self.submissions.get(homework=homework)
            if submission.grade is not None:
                return 'graded'
            return 'submitted'
        except HomeworkSubmission.DoesNotExist:
            if homework.due_date < timezone.now().date():
                return 'overdue'
            return 'pending'

    def get_homework_grade(self, homework):
        """Returns homework grade for this homework. If homework is pending, returns 0."""
        try:
            submission = self.submissions.get(homework=homework)
            return submission.grade if submission.grade else 0
        except HomeworkSubmission.DoesNotExist:
            return 0

    def get_subject_records(self, subject):
        """Returns dict {homework: score} for subject"""
        homeworks = self.get_subject_homeworks(subject)
        records = {}

        for homework in homeworks:
            records[homework] = self.get_homework_grade(homework)

        return records

    def get_homework_submission(self, homework):
        """Returns submission for specific homework if exists."""
        try:
            return self.submissions.get(homework=homework)
        except HomeworkSubmission.DoesNotExist:
            return None

    def get_subject_gpa_with_zeros(self, subject):
        """GPA zeros considered for this subject."""
        records = self.get_subject_records(subject)
        if not records:
            return 0

        total_grade = sum(records.values())
        return total_grade / len(records)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    teacher_number = models.CharField(max_length=20, unique=True)
    subjects = models.ManyToManyField(
        Subject,
        related_name='teachers',
        blank=True
    )

    def get_taught_subjects(self):
        """Returns all taught subjects for this teacher."""
        return self.subjects.all()

    def get_teaching_classes(self):
        """Returns all classes that have this teacher's subjects."""
        return SchoolClass.objects.filter(
            subjects__in=self.subjects.all()
        ).distinct()

    def get_assigned_homeworks(self):
        """Returns all homeworks assigned by this teacher."""
        return Homework.objects.filter(
            subject__in=self.subjects.all()
        ).order_by('-due_date')

    def get_subject_homeworks(self, subject):
        """Returns homeworks for specific subject."""
        if subject not in self.subjects.all():
            return Homework.objects.none()
        return Homework.objects.filter(subject=subject)

    def get_ungraded_submissions(self):
        """Returns all ungraded submissions for this teacher."""
        return HomeworkSubmission.objects.filter(
            homework__subject__in=self.subjects.all(),
            grade__isnull=True
        ).order_by('date_submitted')

    def get_homework_submissions(self, homework):
        """Returns all submissions for specific homework."""
        if homework.subject not in self.subjects.all():
            return HomeworkSubmission.objects.none()
        return homework.submissions.all().order_by('date_submitted')

    def get_today_submissions(self):
        """Returns submissions made today."""
        return HomeworkSubmission.objects.filter(
            homework__subject__in=self.subjects.all(),
            date_submitted=timezone.now().date()
        )

    def get_homework_statistics(self, homework):
        """Returns statistics for specific homework."""
        if homework.subject not in self.subjects.all():
            return None

        submissions = self.get_homework_submissions(homework)
        total_students = homework.school_class.students.count()
        graded = submissions.filter(grade__isnull=False).count()
        ungraded = submissions.filter(grade__isnull=True).count()
        submitted = submissions.count()
        not_submitted = total_students - submitted

        return {
            'total_students': total_students,
            'submitted': submitted,
            'not_submitted': not_submitted,
            'graded': graded,
            'ungraded': ungraded,
            'submission_rate': (submitted / total_students * 100) if total_students > 0 else 0,
            'grading_rate': (graded / submitted * 100) if submitted > 0 else 0,
        }

    def can_grade_submission(self, submission):
        """Check if teacher can grade this submission."""
        return submission.homework.subject in self.subjects.all()

    def can_grade_homework(self, homework):
        """Check if teacher can access this homework."""
        return homework.subject in self.subjects.all()

    def get_students_count(self):
        """Returns total number of students in teacher's classes."""
        return Student.objects.filter(
            school_class__in=self.get_teaching_classes()
        ).count()

    def __str__(self):
        return self.user.get_full_name()


class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='homeworks')
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='homeworks')
    date_assigned = models.DateField()
    due_date = models.DateField()
    text = models.TextField()
    penalty_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject.name} — {self.school_class.name}"

    @property
    def is_overdue(self):
        """Check if homework is overdue."""
        return timezone.now().date() > self.due_date

    @property
    def days_until_due(self):
        """Returns days until due date (negative if overdue)."""
        return (self.due_date - timezone.now().date()).days

    @property
    def submission_count(self):
        """Returns number of submissions."""
        return self.submissions.count()

    @property
    def graded_count(self):
        """Returns number of graded submissions."""
        return self.submissions.filter(grade__isnull=False).count()

    @property
    def submission_rate(self):
        """Returns submission rate as percentage."""
        total_students = self.school_class.students.count()
        if total_students == 0:
            return 0
        return (self.submission_count / total_students) * 100

    def get_ungraded_submissions(self):
        """Returns ungraded submissions."""
        return self.submissions.filter(grade__isnull=True)

    def get_class_students(self):
        """Returns students in this class."""
        return self.school_class.students.all()

    def get_students_who_submitted(self):
        """Returns students who submitted this homework."""
        return Student.objects.filter(
            submissions__homework=self
        ).distinct()

    def get_students_who_did_not_submit(self):
        """Returns students who didn't submit this homework."""
        submitted_students = self.get_students_who_submitted()
        return self.school_class.students.exclude(
            id__in=submitted_students.values_list('id', flat=True)
        )

    def can_be_graded_by(self, teacher):
        """Check if teacher can grade this submission."""
        return self.homework.subject in teacher.subjects.all()


class HomeworkSubmission(models.Model):
    GRADE_CHOICES = (
        (2, 'F'),
        (3, 'D'),
        (4, 'B'),
        (5, 'A'),
    )

    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submitted_text = models.TextField()
    date_submitted = models.DateField(auto_now_add=True)
    grade = models.IntegerField(choices=GRADE_CHOICES, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    last_edited = models.DateTimeField(auto_now=True)
    was_graded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} → {self.homework.subject.name}"

    @property
    def is_graded(self):
        """Check if submission is graded."""
        return self.grade is not None

    @property
    def is_late(self):
        """Check if submission is late."""
        return self.date_submitted > self.homework.due_date

    @property
    def days_late(self):
        """Returns days late (0 if on time)."""
        if self.is_late:
            return (self.date_submitted - self.homework.due_date).days
        return 0

    def get_grade_display(self):
        """Returns grade as letter."""
        if self.grade:
            return dict(self.GRADE_CHOICES).get(self.grade, 'N/A')
        return 'Not graded'

    def can_be_graded_by(self, teacher):
        """Check if teacher can grade this submission."""
        return self.homework.subject in teacher.subjects.all()

    def reset_grade_on_edit(self):
        """Discards grade on edit."""
        if self.grade is not None:
            self.was_graded = True
            self.grade = None
            self.feedback = ""
            self.save()

    @property
    def is_new_version(self):
        """Returns true if submission is unread."""
        return self.was_graded and self.grade is None

    def mark_as_graded(self, grade, feedback):
        """Marks submission as graded."""
        self.grade = grade
        self.feedback = feedback
        self.was_graded = True
        self.save()
