from django.db.models import Min, Max, Count
from owners.models import CarOwner, Car, DriverLicense, Ownership


def print_header(title):
    print('\n' + '=' * 10 + ' ' + title + ' ' + '=' * 10)


def run_aggregate_queries():
    # 1. Дата выдачи самого старшего водительского удостоверения
    print_header('1. Самая ранняя дата выдачи удостоверения')
    oldest_issue = DriverLicense.objects.aggregate(
        oldest=Min('issue_date')
    )['oldest']
    print('Самое старое удостоверение выдано:', oldest_issue)

    # 2. Самая поздняя дата владения машиной (по start_date в Ownership)
    print_header('2. Самая поздняя дата начала владения машиной')
    latest_ownership = Ownership.objects.aggregate(
        latest=Max('start_date')
    )['latest']
    print('Самая поздняя дата начала владения:', latest_ownership)

    # 3. Количество машин для каждого водителя
    print_header('3. Количество машин у каждого владельца')
    owners_with_car_count = CarOwner.objects.annotate(
        car_count=Count('cars', distinct=True)   # через ManyToMany cars
    )
    for owner in owners_with_car_count:
        print(f'{owner.id}: {owner.last_name} {owner.first_name} — {owner.car_count} машин(ы)')

    # 4. Количество машин каждой марки
    print_header('4. Количество машин каждой марки')
    cars_per_brand = Car.objects.values('brand').annotate(
        count=Count('id')
    )
    for row in cars_per_brand:
        print(f'{row["brand"]}: {row["count"]} шт.')

    # 5. Все автовладельцы, отсортированные по дате выдачи удостоверения
    print_header('5. Владельцы, отсортированные по дате выдачи первого удостоверения')
    owners_by_license_date = CarOwner.objects.annotate(
        first_license_date=Min('licenses__issue_date')
    ).order_by('first_license_date').distinct()

    for owner in owners_by_license_date:
        print(f'{owner.id}: {owner.last_name} {owner.first_name} — {owner.first_license_date}')


run_aggregate_queries()

# для запуска
# exec(open('3_1_3_queries.py', encoding='utf-8').read())