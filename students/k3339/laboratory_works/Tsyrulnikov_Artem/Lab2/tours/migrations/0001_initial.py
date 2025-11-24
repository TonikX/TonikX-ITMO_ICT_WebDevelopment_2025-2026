from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Tour",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("agency", models.CharField(max_length=120)),
                ("description", models.TextField()),
                ("country", models.CharField(max_length=80)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("payment_terms", models.TextField()),
            ],
            options={
                "ordering": ["start_date"],
            },
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("guests", models.PositiveSmallIntegerField(default=1)),
                ("travel_start", models.DateField()),
                ("travel_end", models.DateField()),
                ("status", models.CharField(choices=[("pending", "В ожидании"), ("confirmed", "Подтверждено"), ("cancelled", "Отменено")], default="pending", max_length=12)),
                ("reserved_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("tour", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="tours.tour")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-reserved_at"],
                "unique_together": {("user", "tour", "travel_start", "travel_end")},
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tour_start", models.DateField()),
                ("tour_end", models.DateField()),
                ("text", models.TextField()),
                ("rating", models.PositiveSmallIntegerField()),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ("tour", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="tours.tour")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
