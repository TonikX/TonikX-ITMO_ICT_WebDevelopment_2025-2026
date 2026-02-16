from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raceapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='racer',
            name='is_confirmed',
            field=models.BooleanField(default=False, verbose_name='Подтверждено'),
        ),
    ]