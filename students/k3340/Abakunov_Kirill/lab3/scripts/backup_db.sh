#!/bin/bash
# Скрипт для создания резервной копии базы данных

BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/hotel_db_$DATE.sql"

echo "=== Создание резервной копии базы данных ==="
echo ""

# Создаем папку для бэкапов
mkdir -p $BACKUP_DIR

# Проверяем, запущен ли Docker Compose
if ! docker-compose ps | grep -q "db"; then
    echo "Ошибка: PostgreSQL не запущен"
    echo "Запустите: docker-compose up -d"
    exit 1
fi

echo "Создание резервной копии..."
docker-compose exec -T db pg_dump -U hotel_user hotel_db > $BACKUP_FILE

if [ $? -eq 0 ]; then
    SIZE=$(du -h $BACKUP_FILE | cut -f1)
    echo "✓ Резервная копия создана: $BACKUP_FILE ($SIZE)"
    echo ""
    echo "Список резервных копий:"
    ls -lh $BACKUP_DIR/
else
    echo "✗ Ошибка при создании резервной копии"
    exit 1
fi

echo ""
echo "Для восстановления используйте:"
echo "  cat $BACKUP_FILE | docker-compose exec -T db psql -U hotel_user hotel_db"
