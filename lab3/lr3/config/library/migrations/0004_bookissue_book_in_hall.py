# Generated manually

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0003_alter_bookissue_issue_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookissue",
            name="book_in_hall",
            field=models.ForeignKey(
                blank=True,
                help_text="Из какого зала выдана книга (для учёта копий)",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="library.bookinhall",
            ),
        ),
    ]
