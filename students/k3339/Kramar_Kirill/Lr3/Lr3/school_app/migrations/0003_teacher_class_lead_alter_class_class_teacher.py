import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0002_alter_lesson_weekday_alter_student_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='class_lead',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_lead_teacher', to='school_app.class'),
        ),
        migrations.AlterField(
            model_name='class',
            name='class_teacher',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_teacher_of_class', to='school_app.teacher'),
        ),
    ]
