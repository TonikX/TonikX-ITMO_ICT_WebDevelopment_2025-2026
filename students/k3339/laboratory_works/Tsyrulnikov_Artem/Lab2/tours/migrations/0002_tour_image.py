from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="tour",
            name="image",
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tour",
            name="image_mime",
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
