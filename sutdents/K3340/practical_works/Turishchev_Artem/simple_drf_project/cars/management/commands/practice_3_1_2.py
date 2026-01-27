from django.core.management.base import BaseCommand

from cars.models import CarOwner, Car, DriverLicense


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(f'Все машины марки Toyta:\n{"\n".join(map(str, Car.objects.filter(brand="Toyota")))}')
        print("********************************")
        self.stdout.write(f'Все водители с именем “Олег”:\n{"\n".join(map(str, CarOwner.objects.filter(name="Олег")))}')
        print("********************************")
        random_owner_id = CarOwner.objects.order_by('?').first().id
        self.stdout.write(f'Права случайного водителя:\n{"\n".join(map(str, DriverLicense.objects.filter(owner_id=random_owner_id)))}')
        print("********************************")
        self.stdout.write(f'Все владельцы белых машин:\n{"\n".join(map(str, CarOwner.objects.filter(cars__color="White")))}')
        print("********************************")
        self.stdout.write(f'Все владельцы, чей год владения машиной начинается с 2010 :\n{"\n".join(map(str, CarOwner.objects.filter(ownership__start_date__year=2010).distinct()))}')
