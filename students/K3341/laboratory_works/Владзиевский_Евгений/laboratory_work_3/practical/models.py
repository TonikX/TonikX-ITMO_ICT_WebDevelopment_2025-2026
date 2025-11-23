import django
from django.conf import settings
from django.db import connection, models


def configure_settings():
    if settings.configured:
        return

    settings.configure(
        INSTALLED_APPS=["django.contrib.contenttypes"],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "lab3.sqlite3",
            }
        },
        TIME_ZONE="UTC",
        USE_TZ=False,
        DEFAULT_AUTO_FIELD="django.db.models.AutoField",
    )
    django.setup()


configure_settings()


class CarOwner(models.Model):
    id = models.IntegerField(primary_key=True, db_column="Id_владельца")
    last_name = models.CharField(max_length=30, db_column="Фамилия")
    first_name = models.CharField(max_length=30, db_column="Имя")
    birth_date = models.DateTimeField(null=True, db_column="Дата_рождения")

    cars = models.ManyToManyField("Car", through="Ownership", related_name="owners")

    class Meta:
        app_label = "lab3"
        db_table = "Автовладелец"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Car(models.Model):
    id = models.IntegerField(primary_key=True, db_column="Id_автомобиля")
    plate_number = models.CharField(max_length=15, db_column="Гос_номер")
    brand = models.CharField(max_length=20, db_column="Марка")
    model = models.CharField(max_length=20, db_column="Модель")
    color = models.CharField(max_length=30, null=True, db_column="Цвет")

    class Meta:
        app_label = "lab3"
        db_table = "Автомобиль"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number})"


class Ownership(models.Model):
    id = models.IntegerField(primary_key=True, db_column="Id_владелец_авто")
    owner = models.ForeignKey(
        CarOwner,
        on_delete=models.CASCADE,
        null=True,
        db_column="Id_владельца",
        related_name="ownerships",
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        null=True,
        db_column="Id_автомобиля",
        related_name="ownerships",
    )
    start_date = models.DateTimeField(db_column="Дата_начала")
    end_date = models.DateTimeField(null=True, db_column="Дата_окончания")

    class Meta:
        app_label = "lab3"
        db_table = "Владение"

    def __str__(self):
        return f"{self.owner} -> {self.car}"


class License(models.Model):
    id = models.IntegerField(primary_key=True, db_column="Id_удостоверения")
    owner = models.ForeignKey(
        CarOwner,
        on_delete=models.CASCADE,
        db_column="Id_владельца",
        related_name="licenses",
    )
    license_number = models.CharField(max_length=10, db_column="Номер_удостоверения")
    license_type = models.CharField(max_length=10, db_column="Тип")
    issue_date = models.DateTimeField(db_column="Дата_выдачи")

    class Meta:
        app_label = "lab3"
        db_table = "Водительское_удостоверение"

    def __str__(self):
        return f"{self.license_number} ({self.license_type})"


def ensure_tables():
    existing = set(connection.introspection.table_names())
    models_to_create = []

    for model in (CarOwner, Car, Ownership, License):
        if model._meta.db_table not in existing:
            models_to_create.append(model)

    if not models_to_create:
        return

    with connection.schema_editor() as schema_editor:
        for model in models_to_create:
            schema_editor.create_model(model)
