#!/bin/bash
# Скрипт для сброса и перезагрузки данных

echo "=== Сброс и перезагрузка данных ==="
echo ""

# Проверяем, запущен ли Docker Compose
if ! docker-compose ps | grep -q "web"; then
    echo "Ошибка: Docker Compose не запущен"
    echo "Запустите: docker-compose up -d"
    exit 1
fi

echo "1. Удаление старых данных..."
docker-compose exec -T web python manage.py shell << EOF
from api.models import Room, Guest, Staff, CleaningSchedule
CleaningSchedule.objects.all().delete()
Guest.objects.all().delete()
Staff.objects.all().delete()
Room.objects.all().delete()
print("✓ Данные удалены")
EOF

echo ""
echo "2. Загрузка новых тестовых данных..."
docker-compose exec -T web python manage.py load_hotel_data

echo ""
echo "=== Данные успешно перезагружены ==="
echo ""
echo "Статистика:"
docker-compose exec -T web python manage.py shell << EOF
from api.models import Room, Guest, Staff, CleaningSchedule
print(f"  - Номеров: {Room.objects.count()}")
print(f"  - Гостей: {Guest.objects.count()}")
print(f"  - Служащих: {Staff.objects.count()}")
print(f"  - Расписаний: {CleaningSchedule.objects.count()}")
EOF
