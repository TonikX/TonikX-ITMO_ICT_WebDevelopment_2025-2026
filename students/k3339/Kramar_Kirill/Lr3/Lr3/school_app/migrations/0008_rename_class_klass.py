from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0007_alter_lesson_classroom_alter_lesson_lesson_number'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Class',
            new_name='Klass',
        ),
    ]
