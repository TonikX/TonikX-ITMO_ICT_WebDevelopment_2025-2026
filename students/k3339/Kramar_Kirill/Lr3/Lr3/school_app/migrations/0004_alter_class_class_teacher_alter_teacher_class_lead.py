import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0003_teacher_class_lead_alter_class_class_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='class_teacher',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school_app.teacher'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='class_lead',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school_app.class'),
        ),
    ]
