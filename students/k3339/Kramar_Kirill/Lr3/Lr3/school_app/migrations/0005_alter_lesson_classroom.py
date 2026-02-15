import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0004_alter_class_class_teacher_alter_teacher_class_lead'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='classroom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='school_app.classroom'),
        ),
    ]
