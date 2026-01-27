# Отчеты

## Backend

Доступные эндпоинты отчетов:
- `GET /api/reports/subject_for_class/?class_id=1&day=1&lesson=2`
- `GET /api/reports/teachers_per_subject/`
- `GET /api/reports/same_subject_teachers/?class_id=1`
- `GET /api/reports/gender_count_per_class/`
- `GET /api/reports/classroom_stats/`
- `GET /api/reports/class_performance_report/?class_id=1&quarter=1&school_year=2025-2026`

## Frontend

Интерфейс отчетов находится в разделе **Отчеты** и включает:
- успеваемость класса;
- статистику по полу;
- статистику по кабинетам;
- учителей по предметам.

Визуализация на графиках отключена, отображаются только таблицы и агрегированные данные.
