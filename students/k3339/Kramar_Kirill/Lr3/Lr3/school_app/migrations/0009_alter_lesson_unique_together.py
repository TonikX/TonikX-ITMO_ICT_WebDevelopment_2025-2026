from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0008_rename_class_klass'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together={('klass', 'weekday', 'lesson_number')},
        ),
    ]
