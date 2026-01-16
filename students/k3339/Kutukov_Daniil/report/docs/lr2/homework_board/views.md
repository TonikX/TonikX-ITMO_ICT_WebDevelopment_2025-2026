# Представления Homework Board

## Классовые представления

- `AssignmentListView` - список заданий
- `AssignmentDetailView` - детализация задания
- `AssignmentCreateView` - создание задания
- `AssignmentUpdateView` - редактирование задания
- `AssignmentDeleteView` - удаление задания

## Функциональные представления

- `submit_assignment` - сдача задания студентом
- `grade_submission` - оценка сдачи преподавателем

## Аутентификация

Используется Django's authentication system с кастомной User моделью.