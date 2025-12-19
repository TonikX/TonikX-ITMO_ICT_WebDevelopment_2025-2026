import os
import django

# Установить настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_project.settings')
django.setup()

from django.db.models import Min, Max, Count
from owners.models import CarOwner, Car, DriverLicense, Ownership


def run_aggregate_queries():

    # 1. Самое старшее водительское удостоверение
    print('1. Самое старшее водительское удостоверение')
    oldest_issue = DriverLicense.objects.aggregate(
        earliest=Min('issue_date')
    )['earliest']
    print('Самое старое удостоверение выдано:', oldest_issue)

    # 2. Самая поздняя дата начала владения машиной
    print('\n2. Самая поздняя дата начала владения машиной')
    latest_ownership = Ownership.objects.aggregate(
        latest=Max('start_date')
    )['latest']
    print('Самая поздняя дата начала владения:', latest_ownership)

    # 3. Количество машин у каждого водителя
    print('\n3. Количество машин у каждого владельца')
    owners_with_car_count = CarOwner.objects.annotate(
        car_count=Count('cars', distinct=True)
    )
    for owner in owners_with_car_count:
        print(f'{owner.id}: {owner.last_name} {owner.first_name} — {owner.car_count} шт.')

    # 4. Количество машин каждой марки
    print('\n4. Количество машин каждой марки')
    cars_per_brand = Car.objects.values('brand').annotate(
        count=Count('id')
    )
    for row in cars_per_brand:
        print(f'{row["brand"]}: {row["count"]} шт.')

    # 5. Сортировка владельцев по дате выдачи удостоверения
    print('\n5. Владельцы, отсортированные по дате выдачи удостоверения')
    owners_by_license_date = CarOwner.objects.annotate(
        first_license_date=Min('licenses__issue_date')
    ).order_by('first_license_date').distinct()

    for owner in owners_by_license_date:
        print(f'{owner.id}: {owner.last_name} {owner.first_name} — {owner.first_license_date}')


run_aggregate_queries()

