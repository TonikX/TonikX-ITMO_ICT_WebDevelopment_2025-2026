# Модель данных

## Сущности
- **Subject** — предмет.
  - `name: str`
- **Homework** — домашнее задание.
  - `subject: FK --> Subject`
  - `teacher: FK --> User`
  - `given_at: date`
  - `due_from: date`, `due_to: date`
  - `penalty_info: str?`
  - `text: Text`
- **Submission** — сдача студента по ДЗ.
  - `homework: FK --> Homework`
  - `student: FK --> User`
  - `body: Text`
  - `score: int?` (оценка)
  - `created_at/updated_at: datetime`
- **Review** — отзыв на ДЗ.
  - `homework: FK --> Homework`
   - `author: FK --> User`
  - `rating: int (1 до 10 включительно)`
  - `text: Text`

Таким образом, мы получаем нормализованные связи «один-ко-многим» удобны для фильтров и пагинации.
`Submission` отделён от `Review`, чтобы отзывы могли оставлять и другие студенты.
Храним `teacher` у `Homework` чтобы было легко фильтровать ДЗ по преподавателю.
