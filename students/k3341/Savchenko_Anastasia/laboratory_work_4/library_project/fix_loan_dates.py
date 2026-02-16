# fix_loan_dates.py
import os
import sys
import django
from datetime import date, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from library_app.models import LoanRecord

print("Исправление дат выдачи в существующих записях...")
print("=" * 50)

# Список всех выдач с их ID
loans = LoanRecord.objects.all()
dates_to_set = [
    date(2026, 1, 1),  # 35 дней назад от 2026-02-04
    date(2026, 1, 15),  # 20 дней назад
    date(2026, 1, 10),  # 25 дней назад
    date(2026, 1, 5),  # 30 дней назад
    date(2026, 1, 20),  # 15 дней назад
    date(2025, 12, 20),  # 46 дней назад
    date(2025, 12, 25),  # 41 день назад
]

for i, loan in enumerate(loans):
    if i < len(dates_to_set):
        new_date = dates_to_set[i]
        loan.issued_at = new_date
        loan.save()

        print(f"Выдача ID {loan.loan_id}:")
        print(f"  Читатель: {loan.reader_id.full_name}")
        print(f"  Книга: {loan.copy_book_id.book_id.title}")
        print(f"  Новая дата выдачи: {new_date}")
        print(f"  Дней назад: {(date.today() - new_date).days}")
        print()

print("=" * 50)
print("✅ Даты исправлены!")

# Проверяем просроченные
print("\nПроверка просроченных выдач (>30 дней):")
month_ago = date.today() - timedelta(days=30)
overdue_loans = LoanRecord.objects.filter(
    issued_at__lt=month_ago,
    returned_at__isnull=True
)

print(f"Найдено просроченных: {overdue_loans.count()}")
for loan in overdue_loans:
    print(f"  • {loan.reader_id.full_name}: {loan.copy_book_id.book_id.title} (выдана {loan.issued_at})")