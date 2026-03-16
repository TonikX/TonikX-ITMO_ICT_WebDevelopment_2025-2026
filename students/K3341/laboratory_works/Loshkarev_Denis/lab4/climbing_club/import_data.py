import os
import django
import csv
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from climbing_app.models import Club, Alpinist, Mountain, Route, Climb, Participation


def run_import():
    Participation.objects.all().delete()
    Climb.objects.all().delete()
    Route.objects.all().delete()
    Alpinist.objects.all().delete()
    Mountain.objects.all().delete()
    Club.objects.all().delete()

    with open('data/clubs.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Club.objects.create(**row)

    with open('data/mountains.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Mountain.objects.create(**row)

    with open('data/alpinists.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            club = Club.objects.get(name=row['club_name'])
            alp = Alpinist.objects.create(name=row['name'], address=row['address'])
            alp.clubs.add(club)  # M2M — .add() вместо club=club

    with open('data/routes.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mtn = Mountain.objects.get(name=row['mountain_name'])
            Route.objects.create(
                mountain=mtn,
                description=row['description'],
                expected_duration=timedelta(hours=int(row['expected_duration_hours']))
            )

    with open('data/climbs.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            route = Route.objects.filter(mountain__name=row['route_mountain']).first()
            if route:
                Climb.objects.create(
                    group_name=row['group_name'],
                    route=route,
                    start_planned=row['start_actual'],
                    end_planned=row['end_actual'],
                    start_actual=row['start_actual'],
                    end_actual=row['end_actual'],
                    is_group_success=(row['is_group_success'] == 'True')
                )

    with open('data/participations.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            alp = Alpinist.objects.get(name=row['alpinist_name'])
            climb = Climb.objects.get(group_name=row['group_name'])
            Participation.objects.create(
                alpinist=alp,
                climb=climb,
                is_success=(row['is_success'] == 'True'),
                status=row['status'],
                incident_details=row['incident_details']
            )

    print("Данные успешно импортированы из CSV!")


if __name__ == "__main__":
    run_import()