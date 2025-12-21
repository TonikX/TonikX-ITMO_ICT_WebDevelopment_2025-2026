from django.db.models import Count, Min, Max
from autoapp.models import *

# 1. Самая старая дата выдачи удостоверения
oldest_license = License.objects.aggregate(oldest=Min('issue_date'))
print("Oldest license issue date:", oldest_license['oldest'])

# 2. Самая поздняя дата владения машиной (для модели "Camry")
latest_ownership = Ownership.objects.filter(car__model="Camry").aggregate(latest=Max('start_date'))
print("Latest ownership for Camry:", latest_ownership['latest'])

# 3. Количество машин у каждого владельца
owners_with_car_count = Owner.objects.annotate(car_count=Count('ownerships__car', distinct=True))
for owner in owners_with_car_count:
    print(f"{owner}: {owner.car_count} cars")

# 4. Количество машин каждой марки
cars_by_brand = Car.objects.values('brand').annotate(count=Count('id'))
for item in cars_by_brand:
    print(f"{item['brand']}: {item['count']}")

# 5. Сортировка владельцев по дате выдачи удостоверения (самые старые первыми)
owners_sorted = Owner.objects.filter(licenses__isnull=False).order_by('licenses__issue_date').distinct()
print("Owners sorted by license issue date:", list(owners_sorted))