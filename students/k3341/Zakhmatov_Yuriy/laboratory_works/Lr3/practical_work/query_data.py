from autoapp.models import *

# 1. Все машины марки "Toyota"
toyota_cars = Car.objects.filter(brand="Toyota")
print("Toyota cars:", list(toyota_cars))

# 2. Все водители с именем "Олег"
oleg_owners = Owner.objects.filter(first_name="Олег")
print("Owners named Oleg:", list(oleg_owners))

# 3. Получить случайного владельца и его удостоверение
import random
random_owner = Owner.objects.order_by('?').first()
license = License.objects.get(owner=random_owner)
print(f"Random owner: {random_owner}, License: {license}")

# 4. Все владельцы красных машин
red_car_owners = Owner.objects.filter(ownerships__car__color="Красный").distinct()
print("Owners of red cars:", list(red_car_owners))

# 5. Все владельцы, чье владение машиной началось с 2017 года
owners_from_2017 = Owner.objects.filter(ownerships__start_date__year=2017).distinct()
print("Owners from 2017:", list(owners_from_2017))