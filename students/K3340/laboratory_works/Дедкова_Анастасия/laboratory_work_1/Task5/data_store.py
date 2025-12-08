"""
Формат файла grades.json:
{
  "Математика": ["5", "4"],
  "Физика": ["0,01"]
}
"""

import json
import os
from typing import Dict, List

FILE_PATH = "grades.json"


def _load() -> Dict[str, List[str]]:
    """Загружаем словарь дисциплин и оценок из JSON, если файла нет — пустой словарь."""
    if not os.path.exists(FILE_PATH):
        return {}
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save(data: Dict[str, List[str]]) -> None:
    """Сохраняем словарь в JSON."""
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_grade(discipline: str, grade: str) -> None:
    """Добавляем оценку к дисциплине."""
    data = _load()
    discipline = discipline.strip()
    grade = grade.strip()
    if not discipline or not grade:
        return
    data.setdefault(discipline, []).append(grade)
    _save(data)


def get_all() -> Dict[str, List[str]]:
    """Возвращаем весь журнал."""
    return _load()
