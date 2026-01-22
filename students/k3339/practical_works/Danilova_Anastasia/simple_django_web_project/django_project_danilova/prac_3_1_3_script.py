from django.db.models import Count, Min, Max
from project_first_app.models import *

# 1. Вывод даты выдачи самого старшего водительского удостоверения
print("\n1. ДАТА ВЫДАЧИ САМОГО СТАРШЕГО ВОДИТЕЛЬСКОГО УДОСТОВЕРЕНИЯ:")
print("-" * 40)

oldest_license = DriversLicense.objects.aggregate(
    oldest_date=Min('date_of_issue')
)

if oldest_license['oldest_date']:
    license_obj = DriversLicense.objects.filter(
        date_of_issue=oldest_license['oldest_date']
    ).first()

    print(f"Самое старое удостоверение выдано: {oldest_license['oldest_date']}")
    if license_obj:
        print(f"Подробности:")
        print(f"Владелец: {license_obj.car_owner}")
        print(f"Номер: {license_obj.license_number}")
        print(f"Тип: {license_obj.license_type}")
else:
    print("Нет данных об удостоверениях")

# 2. Самая поздняя дата владения машиной для существующей модели
print("\n\n2. САМАЯ ПОЗДНЯЯ ДАТА ВЛАДЕНИЯ МАШИНОЙ (ДЛЯ СУЩЕСТВУЮЩИХ МОДЕЛЕЙ):")
print("-" * 40)

models = Car.objects.values_list('model', flat=True).distinct()

if models:
    latest_dates = []

    for model_name in models:
        model_latest = Ownership.objects.filter(
            car__model=model_name
        ).aggregate(
            latest=Max('date_started')
        )

        if model_latest['latest']:
            latest_dates.append({
                'model': model_name,
                'date': model_latest['latest'],
                'ownerships': Ownership.objects.filter(
                    car__model=model_name,
                    date_started=model_latest['latest']
                )
            })

    if latest_dates:
        latest_overall = max(latest_dates, key=lambda x: x['date'])

        print(f"Самая поздняя дата владения: {latest_overall['date']}")
        print(f"Модель: {latest_overall['model']}")
        print(f"Количество записей с этой датой: {latest_overall['ownerships'].count()}")

        # Показываем все записи с этой датой
        for i, ownership in enumerate(latest_overall['ownerships'], 1):
            print(f"     {i}. {ownership.car_owner} -> {ownership.car} (дата начала: {ownership.date_started})")
    else:
        print("Нет данных о владении")
else:
    print("В базе нет моделей автомобилей")

# 3. Количество машин для каждого водителя
print("\n\n3. КОЛИЧЕСТВО МАШИН ДЛЯ КАЖДОГО ВОДИТЕЛЯ:")
print("-" * 40)

owners_with_car_count = CarOwner.objects.annotate(
    total_cars=Count('ownerships__car', distinct=True)
).order_by('-total_cars')

if owners_with_car_count.exists():
    print(f"Всего владельцев: {owners_with_car_count.count()}")
    print(f"  {'=' * 40}")

    for owner in owners_with_car_count:
        if owner.total_cars > 0:
            cars = Car.objects.filter(ownerships__car_owner=owner).distinct()
            car_list = [f"{car.brand} {car.model}" for car in cars]

            print(f"{owner.first_name} {owner.last_name}")
            print(f"Количество машин: {owner.total_cars}")
            print(f"Список: {', '.join(car_list)}")
            print(f"     {'-' * 30}")
else:
    print("Нет данных о владельцах")

# 4. Количество машин каждой марки
print("\n\n4. КОЛИЧЕСТВО МАШИН КАЖДОЙ МАРКИ:")
print("-" * 40)

brand_counts = Car.objects.values('brand').annotate(
    total=Count('id')
).order_by('-total')

if brand_counts.exists():
    print(f"Всего марок: {brand_counts.count()}")
    print(f"  {'=' * 40}")

    total_all_cars = 0
    for brand in brand_counts:
        total_all_cars += brand['total']
        print(f"{brand['brand']}: {brand['total']} машин(ы)")

        models_of_brand = Car.objects.filter(
            brand=brand['brand']
        ).values('model').annotate(
            model_count=Count('id')
        )

        for model in models_of_brand:
            print(f"{model['model']}: {model['model_count']}")

    print(f"  {'=' * 40}")
    print(f"Всего автомобилей в базе: {total_all_cars}")
else:
    print("Нет данных об автомобилях")

# 5. Сортировка автовладельцев по дате выдачи удостоверения
print("\n\n5. АВТОВЛАДЕЛЬЦЫ, ОТСОРТИРОВАННЫЕ ПО ДАТЕ ВЫДАЧИ УДОСТОВЕРЕНИЯ:")
print("-" * 40)

owners_sorted = CarOwner.objects.filter(
    licenses__isnull=False
).annotate(
    license_date=Min('licenses__date_of_issue')
).order_by('license_date').distinct()

if owners_sorted.exists():
    print(f"Владельцы с удостоверениями: {owners_sorted.count()}")
    print(f"  {'=' * 40}")

    for i, owner in enumerate(owners_sorted, 1):
        licenses = DriversLicense.objects.filter(car_owner=owner).order_by('date_of_issue')

        print(f"  {i}. {owner.first_name} {owner.last_name}")
        print(f"Дата рождения: {owner.date_of_birth}")

        for j, license in enumerate(licenses, 1):
            status = "САМОЕ РАННЕЕ" if j == 1 else ""
            print(f"Удостоверение {j}: №{license.license_number}, "
                  f"тип {license.license_type}, "
                  f"выдано {license.date_of_issue} {status}")

        if i < len(owners_sorted):
            print(f"     {'-' * 30}")
else:
    print("Нет владельцев с удостоверениями")