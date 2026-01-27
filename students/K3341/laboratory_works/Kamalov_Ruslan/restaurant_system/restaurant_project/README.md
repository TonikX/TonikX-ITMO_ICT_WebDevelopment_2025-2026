# Restaurant API

## Авторизация

```bash
# Регистрация
POST /api/auth/users/
{"username": "user", "password": "pass123", "re_password": "pass123"}

# Логин
POST /api/auth/token/login/
{"username": "user", "password": "pass123"}
→ {"auth_token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"}

# Заголовок для защищенных запросов
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## Должности

```bash
GET /api/positions/
→ {"results": [{"id": 1, "position": "Шеф-повар", "minimum_wage": "80000.00"}]}

POST /api/positions/
{"position": "Официант", "minimum_wage": "45000.00"}
→ {"id": 2, "position": "Официант", "minimum_wage": "45000.00"}
```

## Сотрудники

```bash
GET /api/employees/
→ {"results": [{"id": 1, "full_name": "Иванов И.И.", "category": "chef", "position_name": "Шеф-повар", "salary": "85000.00"}]}

POST /api/employees/
{"full_name": "Петров П.П.", "passport_data": "1234 567890", "category": "waiter", "position": 2, "salary": "50000.00"}
```

## Ингредиенты

```bash
GET /api/ingredients/
→ {"results": [{"id": 1, "name": "Говядина", "stock_quantity": 15.5, "minimum_stock": 10.0, "price_per_unit": "850.00", "is_low_stock": false}]}

POST /api/ingredients/
{"name": "Картофель", "stock_quantity": 25.0, "minimum_stock": 15.0, "price_per_unit": "45.00", "supplier": "ОвощБаза", "ingredient_type": "vegetable"}

GET /api/ingredients/low-stock/
→ {"results": [{"name": "Лук", "stock_quantity": 2.0, "minimum_stock": 5.0}]}
```

## Блюда

```bash
GET /api/dishes/
→ {"results": [{"id": 1, "name": "Стейк", "dish_type": "main", "calculated_price": 357.0, "ingredients_info": [{"ingredient_name": "Говядина", "quantity": 0.3}]}]}

POST /api/dishes/
{"name": "Борщ", "dish_type": "soup"}
```

## Столы

```bash
GET /api/tables/
→ {"results": [{"id": 1, "table_number": 1, "capacity": 4, "status": "free", "waiter_name": "Сидоров С.С."}]}

POST /api/tables/
{"table_number": 5, "capacity": 6, "status": "free", "employee": null}

POST /api/tables/1/status/
{"status": "occupied"}
→ {"id": 1, "status": "occupied", "status_display": "Занят"}
```

## Заказы

```bash
GET /api/orders/
→ {"results": [{"id": 1, "table_number": 1, "status": "received", "total_price": 714.0, "order_details": [{"dish_name": "Стейк", "quantity": 2}]}]}

POST /api/orders/
{"table": 1, "comments": "Без лука", "order_details": [{"dish": 1, "quantity": 2, "special_requests": "Средней прожарки"}]}

POST /api/orders/1/status/
{"status": "cooking"}

GET /api/orders/status/ready/
→ {"results": [{"id": 2, "status": "ready", "table_number": 3}]}
```

## Повара-блюда

```bash
GET /api/chef-dishes/
→ {"results": [{"id": 1, "chef_name": "Иванов И.И.", "dish_name": "Стейк"}]}

POST /api/chef-dishes/
{"employee": 1, "dish": 2}

GET /api/chefs/1/dishes/
→ {"results": [{"id": 1, "name": "Стейк"}, {"id": 2, "name": "Борщ"}]}
```

## Константы

**Категории сотрудников:** `chef`, `cook`, `waiter`  
**Типы ингредиентов:** `meat`, `vegetable`, `dairy`, `spice`, `other`  
**Типы блюд:** `appetizer`, `soup`, `main`, `dessert`, `drink`  
**Статусы столов:** `free`, `occupied`  
**Статусы заказов:** `received`, `cooking`, `ready`, `served`, `paid`