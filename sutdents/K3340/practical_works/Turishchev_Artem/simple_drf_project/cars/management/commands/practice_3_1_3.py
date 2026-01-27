from django.core.management.base import BaseCommand

from cars.models import CarOwner, Car, DriverLicense, Ownership
from django.db.models import Min, Max, Count



class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(f'Самые старые права:\n{DriverLicense.objects.aggregate(Min("issue_date"))["issue_date__min"]}')
        print("********************************")
        self.stdout.write(f'Самая поздняя дата владения:\n{Ownership.objects.aggregate(Max("start_date"))["start_date__max"]}')
        print("********************************")
        owners = CarOwner.objects.annotate(n_cars=Count('cars'))
        ans = ''
        for i in owners:
            ans += f"{str(i)}: {i.n_cars}\n"
        self.stdout.write(f'количество машин для каждого водителя: \n {ans}')
        print("********************************")
        brands = Car.objects.values("brand").annotate(Count("id"))
        ans = ''
        for i in brands:
            ans += f"{i["brand"]}: {i["id__count"]}\n"
        self.stdout.write(f'количество машин для каждой марки: \n {ans}')
        print("********************************")
        owners = CarOwner.objects.order_by("driverlicense__issue_date")
        self.stdout.write(f"Владельцы отсортированные по выдаче прав: \n{"\n".join(map(str, owners))}")