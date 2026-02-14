import os
import django

# Установить настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_project.settings')
django.setup()

from owners.models import CarOwner, Car, DriverLicense, Ownership


def print_header(title):
    print('\n' + '=' * 10, title, '=' * 10)


def run_queries():
    # 1. Все машины марки "Nissan"
    print_header('1. Все машины марки "Nissan"')
    nissans = Car.objects.filter(brand='Nissan')
    for car in nissans:
        print(f'{car.id}: {car.state_number} — {car.brand} {car.model} ({car.color})')

    # 2. Все водители с именем "Elena"
    print_header('2. Все водители с именем "Elena"')
    elenas = CarOwner.objects.filter(first_name='Elena')
    for owner in elenas:
        print(f'{owner.id}: {owner.last_name} {owner.first_name}')

    # 3. Взять любого владельца, получить его id и по нему удостоверение
    print_header('3. Случайный владелец и его удостоверение')
    owner = CarOwner.objects.first()
    if owner is None:
        print('В базе нет ни одного владельца.')
    else:
        print(f'Владелец: id={owner.id}, {owner.last_name} {owner.first_name}')
        try:
            # Получение удостоверения по owner_id
            license_obj = DriverLicense.objects.get(owner_id=owner.id)
            print(f'Удостоверение: {license_obj.license_number}, '
                  f'тип {license_obj.license_type}, '
                  f'дата выдачи {license_obj.issue_date}')
        except DriverLicense.DoesNotExist:
            print('У этого владельца нет удостоверения.')

    # 4. Найти всех владельцев красных машин (у нас красная Mazda CX-5)
    print_header('4. Владельцы красных машин (color="red")')
    red_owners = CarOwner.objects.filter(cars__color='red').distinct()
    for owner in red_owners:
        print(f'{owner.id}: {owner.last_name} {owner.first_name}')

    # 5. Найти владельцев, начавших владеть машиной в 2019 году
    print_header('5. Владельцы, начавшие владение машиной в 2019 году')
    owners_2019 = CarOwner.objects.filter(
        ownerships__start_date__year=2019
    ).distinct()
    for owner in owners_2019:
        print(f'{owner.id}: {owner.last_name} {owner.first_name}')


run_queries()


