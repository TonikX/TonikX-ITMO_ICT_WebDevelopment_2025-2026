# Практическая работа 3.2

В этой работе была выполнена интеграция DRF в Django-проект и реализованы следующие задачи:

## 1. Созданы модели:
- Profession  
- Skill  
- Warrior  
- SkillOfWarrior  

## 2. Реализованы сериализаторы (ModelSerializer, вложенные сериализаторы)

## 3. Реализованы API-ендпоинты:
### Получение списка скилов
`GET /war/skills/`

### Создание нового скила
`POST /war/skills/create/`

### Вывод всех воинов + профессии  
`GET /war/warriors/with-professions/`

### Вывод всех воинов + навыки  
`GET /war/warriors/with-skills/`

### Полная информация о воине (id)  
`GET /war/warriors/<id>/full/`

### Удаление воина  
`DELETE /war/warriors/<id>/delete/`

### Частичное обновление воина  
`PATCH /war/warriors/<id>/update/`

## 4. Тестирование API
API протестирован через DRF Browsable API (web-интерфейс). Все запросы работают корректно.
