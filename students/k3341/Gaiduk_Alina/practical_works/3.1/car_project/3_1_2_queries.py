from owners.models import CarOwner, Car, DriverLicense, Ownership


def print_header(title):
    print('\n' + '=' * 10, title, '=' * 10)


def run_queries():
    # 1. Все машины марки "Toyota"
    print_header('1. Все машины марки "Toyota"')
    toyotas = Car.objects.filter(brand='Toyota')
    for car in toyotas:
        print(f'{car.id}: {car.state_number} — {car.brand} {car.model} ({car.color})')

    # 2. Все водители с именем "Ivan"
    print_header('2. Все водители с именем "Ivan"')
    olegs = CarOwner.objects.filter(first_name='Ivan')
    for owner in olegs:
        print(f'{owner.id}: {owner.last_name} {owner.first_name}')

    # 3. Взять любого владельца, получить его id и по нему удостоверение
    print_header('3. Случайный владелец и его удостоверение')
    owner = CarOwner.objects.first()
    if owner is None:
        print('Владельцев нет в базе.')
    else:
        print(f'Владелец: id={owner.id}, {owner.last_name} {owner.first_name}')
        # через FK в DriverLicense
        try:
            license_obj = DriverLicense.objects.get(owner_id=owner.id)
            print(f'Удостоверение: {license_obj.license_number}, тип {license_obj.license_type}, дата {license_obj.issue_date}')
        except DriverLicense.DoesNotExist:
            print('У этого владельца нет удостоверения (в таблице DriverLicense).')

    # 4. Все владельцы красных машин (red)
    print_header('4. Владельцы красных машин (color="red")')
    red_owners = CarOwner.objects.filter(cars__color='red').distinct()
    for owner in red_owners:
        print(f'{owner.id}: {owner.last_name} {owner.first_name}')

    # 5. Владельцы, у кого год начала владения = 2020
    print_header('5. Владельцы, начавшие владение машиной в 2020 году')
    owners_2020 = CarOwner.objects.filter(
        ownerships__start_date__year=2020
    ).distinct()
    for owner in owners_2020:
        print(f'{owner.id}: {owner.last_name} {owner.first_name}')

run_queries()

# Для запуска exec(open('3_1_2_queries.py', encoding='utf-8').read())