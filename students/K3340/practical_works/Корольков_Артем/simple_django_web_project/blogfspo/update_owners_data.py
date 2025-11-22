# update_owners_data.py
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogfspo.settings')
django.setup()

from automobiles.models import Owner


def update_owners_with_new_fields():
    print("Обновление владельцев новыми данными...")

    # Тестовые данные для заполнения
    test_data = [
        {
            'passport_number': '45 01 123456',
            'address': 'г. Москва, ул. Тверская, д. 1, кв. 10',
            'nationality': 'RU'
        },
        {
            'passport_number': '45 02 654321',
            'address': 'г. Санкт-Петербург, Невский пр-т, д. 25, кв. 5',
            'nationality': 'RU'
        },
        {
            'passport_number': '45 03 789012',
            'address': 'г. Минск, ул. Ленина, д. 15, кв. 3',
            'nationality': 'BY'
        },
        {
            'passport_number': '45 04 345678',
            'address': 'г. Алматы, пр. Абылай хана, д. 12, кв. 7',
            'nationality': 'KZ'
        },
        {
            'passport_number': '45 05 901234',
            'address': 'г. Киев, ул. Крещатик, д. 8, кв. 12',
            'nationality': 'UA'
        }
    ]

    owners = Owner.objects.all()
    updated_count = 0

    for i, owner in enumerate(owners):
        if i < len(test_data):
            data = test_data[i]
            owner.passport_number = data['passport_number']
            owner.address = data['address']
            owner.nationality = data['nationality']
            owner.save()
            print(f"✅ Обновлен: {owner.get_full_name()} - {owner.passport_number}")
            updated_count += 1

    print(f"\nОбновлено владельцев: {updated_count}")
    print(f"Всего владельцев в системе: {Owner.objects.count()}")


if __name__ == "__main__":
    update_owners_with_new_fields()