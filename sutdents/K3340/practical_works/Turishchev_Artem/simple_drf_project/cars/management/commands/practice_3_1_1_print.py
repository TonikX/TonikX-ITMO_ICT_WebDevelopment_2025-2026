from django.core.management.base import BaseCommand

from cars.models import CarOwner, Car, DriverLicense


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(f'Все машины:\n{"\n".join(map(str, Car.objects.all()))}')
        print("********************************")
        self.stdout.write(f'Все владельцы:\n{"\n".join(map(str, CarOwner.objects.all()))}')
        print("********************************")
        self.stdout.write(f'Все права:\n{"\n".join(map(str, DriverLicense.objects.all()))}')
        print("********************************")
        sample_car = Car.objects.get(license_plate="A111AA")
        self.stdout.write(f'Все владельцы машины {str(sample_car)}:\n{"\n".join(map(str, sample_car.owners.all()))}')