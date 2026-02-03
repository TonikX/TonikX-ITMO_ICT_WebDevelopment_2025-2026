#!/bin/bash
# Скрипт для быстрого тестирования API

BASE_URL="http://localhost:8000"
echo "=== Тестирование Hotel Management API ==="
echo ""

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для проверки ответа
check_response() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ OK${NC}"
    else
        echo -e "${RED}✗ FAIL${NC}"
    fi
}

# 1. Проверка доступности API
echo -e "${BLUE}1. Проверка доступности API...${NC}"
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/" | grep -q "200"
check_response

# 2. Получение токена
echo -e "\n${BLUE}2. Получение токена аутентификации...${NC}"
TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/token/login/" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' \
  | grep -o '"auth_token":"[^"]*"' \
  | cut -d'"' -f4)

if [ -n "$TOKEN" ]; then
    echo -e "${GREEN}✓ Токен получен: ${TOKEN:0:20}...${NC}"
else
    echo -e "${RED}✗ Не удалось получить токен${NC}"
    exit 1
fi

# 3. Список номеров
echo -e "\n${BLUE}3. Получение списка номеров...${NC}"
ROOMS=$(curl -s "$BASE_URL/api/rooms/" | grep -o '"count":[0-9]*' | cut -d':' -f2)
echo "Найдено номеров: $ROOMS"
[ "$ROOMS" -gt 0 ] && echo -e "${GREEN}✓ OK${NC}" || echo -e "${RED}✗ FAIL${NC}"

# 4. Свободные номера
echo -e "\n${BLUE}4. Получение свободных номеров...${NC}"
FREE_ROOMS=$(curl -s "$BASE_URL/api/rooms/available/" | grep -o '"count":[0-9]*' | cut -d':' -f2)
echo "Свободных номеров: $FREE_ROOMS"
[ "$FREE_ROOMS" -gt 0 ] && echo -e "${GREEN}✓ OK${NC}" || echo -e "${RED}✗ FAIL${NC}"

# 5. Текущие гости
echo -e "\n${BLUE}5. Получение списка текущих гостей...${NC}"
CURRENT_GUESTS=$(curl -s "$BASE_URL/api/guests/current/" | grep -o '"count":[0-9]*' | cut -d':' -f2)
echo "Проживающих гостей: $CURRENT_GUESTS"
[ "$CURRENT_GUESTS" -ge 0 ] && echo -e "${GREEN}✓ OK${NC}" || echo -e "${RED}✗ FAIL${NC}"

# 6. Список служащих
echo -e "\n${BLUE}6. Получение списка служащих...${NC}"
STAFF=$(curl -s "$BASE_URL/api/staff/" | grep -o '"count":[0-9]*' | cut -d':' -f2)
echo "Найдено служащих: $STAFF"
[ "$STAFF" -gt 0 ] && echo -e "${GREEN}✓ OK${NC}" || echo -e "${RED}✗ FAIL${NC}"

# 7. Гости из Москвы
echo -e "\n${BLUE}7. Поиск гостей из Москвы...${NC}"
MOSCOW_GUESTS=$(curl -s "$BASE_URL/api/guests/from_city/?city=Москва" | grep -o '"count":[0-9]*' | cut -d':' -f2)
echo "Гостей из Москвы: $MOSCOW_GUESTS"
[ "$MOSCOW_GUESTS" -ge 0 ] && echo -e "${GREEN}✓ OK${NC}" || echo -e "${RED}✗ FAIL${NC}"

# 8. Расписание уборки 1 этажа
echo -e "\n${BLUE}8. Расписание уборки 1 этажа...${NC}"
curl -s "$BASE_URL/api/schedules/by_floor/?floor=1" | grep -q "schedules"
check_response

# 9. Swagger документация
echo -e "\n${BLUE}9. Проверка Swagger документации...${NC}"
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/swagger/" | grep -q "200"
check_response

# 10. Квартальный отчет
echo -e "\n${BLUE}10. Получение квартального отчета...${NC}"
REPORT=$(curl -s -H "Authorization: Token $TOKEN" \
  "$BASE_URL/api/reports/quarterly/?year=2024&quarter=1")
echo "$REPORT" | grep -q "total_income"
check_response

echo -e "\n${BLUE}=== Тестирование завершено ===${NC}"
echo ""
echo "Полезные ссылки:"
echo "  - API Root: $BASE_URL/api/"
echo "  - Swagger: $BASE_URL/swagger/"
echo "  - ReDoc: $BASE_URL/redoc/"
echo "  - Admin: $BASE_URL/admin/"
