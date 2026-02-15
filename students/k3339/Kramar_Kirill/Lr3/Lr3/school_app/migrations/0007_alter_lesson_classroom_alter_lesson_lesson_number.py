import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0006_quartergrade_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_app.classroom'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='lesson_number',
            field=models.IntegerField(),
        ),
    ]
