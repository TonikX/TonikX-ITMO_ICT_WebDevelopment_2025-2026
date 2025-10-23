from django import forms
from .models import Submission, Homework, Subject

# форма для сдачи ДЗ студентом
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ("content",)
        widgets = {"content": forms.Textarea(attrs={"rows": 6})}

# форма создания/редактирования ДЗ (для teacher)
class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ("subject", "issued_at", "due_date", "text", "penalty_info")
    # # кастомная валидация полей формы
    def clean(self):
        data = super().clean()
        issued = data.get("issued_at")
        due = data.get("due_date")
        if issued and due and issued > due:
            self.add_error("due_date", "Срок сдачи не может быть раньше даты выдачи.")
        return data

# форма для быстрого добавления предмета
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ("name",)
