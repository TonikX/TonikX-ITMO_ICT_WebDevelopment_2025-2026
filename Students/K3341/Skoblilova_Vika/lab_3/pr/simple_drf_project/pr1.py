import os
import django
from datetime import date
from random import choice, randint
from django.db.models import Count, Min, Max, Avg

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_drf_project.settings')
django.setup()

from autoapp.models import Owner, License, Car, Ownership


def pr1():
    """Практическое задание 1"""

    # Создаем владельцев
    owners = []
    for i in range(6):
        owner = Owner.objects.create(
            last_name=['Surname1', f'Surname{randint(1, 6)}', f'Surname{randint(1, 6)}', f'Surname{randint(1, 6)}', f'Surname{randint(1, 6)}', f'Surname{randint(1, 6)}'][i],
            first_name=['Name1', f'Name{randint(1, 6)}', f'Name{randint(1, 6)}', f'Name{randint(1, 6)}', f'Name{randint(1, 6)}', f'Name{randint(1, 6)}'][i],
            birth_date=date(2000 + i, i + 1, i + 1)
        )
        owners.append(owner)
        print(f'Создан: {owner}')

    # Создаем автомобили
    cars = []
    for i in range(6):
        car = Car.objects.create(
            number=f'A{i:03}BC{i:02}RU',
            brand=['Car1', f'Car{randint(1, 6)}', f'Car{randint(1, 6)}', f'Car{randint(1, 6)}', f'Car{randint(1, 6)}', f'Car{randint(1, 6)}'][i],
            model=['Model1', f'Model{randint(1, 6)}', f'Model{randint(1, 6)}', f'Model{randint(1, 6)}', f'Model{randint(1, 6)}', f'Model{randint(1, 6)}'][i],
            color=['Color1', f'Color{randint(1, 6)}', f'Color{randint(1, 6)}', f'Color{randint(1, 6)}', f'Color{randint(1, 6)}', f'Color{randint(1, 6)}'][i]
        )
        cars.append(car)
        print(f'Создан: {car}')

    # Создаем удостоверения
    for i, owner in enumerate(owners):
        license_obj = License.objects.create(
            owner=owner,
            number=f'AB{i + 1:06d}',
            type='B' if i % 2 == 0 else 'BC',
            issue_date=date(2010 + i, 1, 15)
        )
        print(f'Создано: {license_obj}')

    # Создаем записи о владении
    ownership_relations = [
        (owners[0], [cars[0], cars[1]], date(2015, 3, 10), date(2020, 5, 15)),
        (owners[1], [cars[2]], date(2018, 7, 22), None),
        (owners[2], [cars[3], cars[4], cars[5]], date(2012, 1, 5), date(2019, 11, 30)),
        (owners[3], [cars[0]], date(2020, 6, 1), None),
        (owners[4], [cars[1], cars[2]], date(2017, 9, 14), date(2021, 2, 28)),
        (owners[5], [cars[4]], date(2019, 4, 3), None),
    ]

    for owner, owner_cars, start_date, end_date in ownership_relations:
        for car in owner_cars:
            ownership = Ownership.objects.create(
                owner=owner,
                car=car,
                start_date=start_date,
                end_date=end_date
            )
            print(f'Создано: {ownership}' )


def pr2():
    """Практическое задание 2"""

    # Получаем первого владельца и используем related_name
    first_owner = Owner.objects.first()
    print(f'Владелец: {first_owner}')

    # Используем related_name='licenses'
    licenses = first_owner.licenses.all()
    print(f'\tЕго удостоверения: {list(licenses)}')

    # Используем related_name='ownerships'
    ownerships = first_owner.ownerships.all()
    print(f'\tЕго записи о владении: {list(ownerships)}')

    # Получаем автомобили через промежуточную модель
    cars = [ownership.car for ownership in ownerships]
    print(f'\tЕго автомобили: {[str(car) for car in cars]}')

    print('Все автомобили Toyota:')
    toyota_cars = Car.objects.filter(brand='Toyota')
    for car in toyota_cars:
        print(f'\t- {car}')

    print('\nВсе владельцы по имени Name1:')
    name1_owners = Owner.objects.filter(first_name='Name1')
    for owner in name1_owners:
        print(f'\t- {owner}')

    print('\nУдостоверение случайного владельца:')
    all_owners = Owner.objects.all()
    random_owner = choice(list(all_owners))
    license_obj = License.objects.filter(owner=random_owner).first()
    print(random_owner, license_obj)

    print('\nВладельцы машин цвета Color1:')
    red_car_owners = Owner.objects.filter(ownerships__car__color='Color1').distinct()
    for owner in red_car_owners:
        red_cars = Car.objects.filter(ownerships__owner=owner, color='Color1').distinct()
        print(f'\t- {owner}: {[str(car) for car in red_cars]}')

    print('\nВладения, начатые с 2015 года:')
    recent_ownerships = Ownership.objects.filter(start_date__year__gte=2015)
    for ownership in recent_ownerships:
        print(f'\t- {ownership}')


def pr3():
    """Практическое задание 3"""
    oldest_license = License.objects.aggregate(oldest_date=Min('issue_date'))
    print(f'\nДата выдачи самого старшего водительского удостоверения: {oldest_license['oldest_date']}')

    latest_ownership = Ownership.objects.filter(car__model='Camry').aggregate(latest_date=Max('start_date'))
    print(f'Самая поздняя дата владения машиной: {latest_ownership['latest_date']}')

    print('\nКоличество машин для каждого водителя:')
    owners_car_count = Owner.objects.annotate(
        car_count=Count('ownerships__car', distinct=True)
    ).order_by('-car_count')
    for owner in owners_car_count:
        print(f'\t- {owner.first_name} {owner.last_name}: {owner.car_count} машин')

    print('\nКоличество машин каждой марки:')
    cars_by_brand = Car.objects.values('brand').annotate(
        count=Count('id')
    ).order_by('-count')
    for brand_data in cars_by_brand:
        print(f'\t- Марка "{brand_data['brand']}": {brand_data['count']} машин')

    print('\nАвтовладельцы, отсортированные по дате выдачи удостоверения:')
    owners_distinct = Owner.objects.filter(
        licenses__isnull=False
    ).order_by('licenses__issue_date').distinct()

    for i, owner in enumerate(owners_distinct, 1):
        license_info = owner.licenses.order_by('issue_date').first()
        print(f'   {i}. {owner.first_name} {owner.last_name}: '
              f'удостоверение от {license_info.issue_date}')


if __name__ == '__main__':
    Ownership.objects.all().delete()
    License.objects.all().delete()
    Car.objects.all().delete()
    Owner.objects.all().delete()

    pr1()
    pr2()
    pr3()
