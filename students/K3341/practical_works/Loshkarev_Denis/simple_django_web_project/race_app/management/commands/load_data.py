import csv
from django.core.management.base import BaseCommand
from race_app.models import User, Race, Registration
from django.utils.dateparse import parse_datetime
from datetime import timedelta

class Command(BaseCommand):
    help = 'Загрузка данных из CSV файлов'

    def handle(self, *args, **kwargs):
        Registration.objects.all().delete()
        Race.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        with open('data/users.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                user, created = User.objects.get_or_create(
                    username=row['username'],
                    defaults={
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'racer_class': row['racer_class'],
                        'experience': int(row['experience']),
                    }
                )
                if created:
                    user.set_password(row['password']) # Хешируем пароль
                    user.save()
        self.stdout.write("Пользователи загружены")

        with open('data/races.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Race.objects.get_or_create(
                    title=row['title'],
                    defaults={
                        'date': parse_datetime(row['date']),
                        'location': row['location']
                    }
                )
        self.stdout.write("Гонки загружены")

        with open('data/registrations.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                user = User.objects.get(username=row['username'])
                race = Race.objects.get(title=row['race_title'])
                
                h, m, s = map(int, row['race_time'].split(':'))
                duration = timedelta(hours=h, minutes=m, seconds=s)

                Registration.objects.get_or_create(
                    user=user,
                    race=race,
                    defaults={
                        'team_name': row['team_name'],
                        'car_description': row['car_description'],
                        'result_place': int(row['result_place']),
                        'race_time': duration
                    }
                )
        self.stdout.write("Результаты и регистрации загружены!")