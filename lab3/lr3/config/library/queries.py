from datetime import timedelta, date
from django.utils import timezone
from .models import Book, Reader, BookIssue


def get_books_by_reader(reader_id):
    issues = BookIssue.objects.filter(reader_id=reader_id)

    books = []
    for issue in issues:
        books.append(issue.book.title)

    return books


def readers_with_old_books():
    month_ago = timezone.now() - timedelta(days=30)

    issues = BookIssue.objects.filter(issue_date__lt=month_ago)

    readers = []
    for issue in issues:
        readers.append(issue.reader.full_name)

    return list(set(readers))


def readers_with_rare_books():
    issues = BookIssue.objects.filter(book__copies__lte=2)

    result = []

    for issue in issues:
        result.append({
            "reader": issue.reader.full_name,
            "book": issue.book.title
        })

    return result


def count_readers_under_20():
    today = date.today()
    readers = Reader.objects.all()

    count = 0

    for reader in readers:
        age = today.year - reader.birth_date.year
        if age < 20:
            count += 1

    return count


def education_statistics():
    readers = Reader.objects.all()
    total = readers.count()

    if total == 0:
        return {}

    primary = readers.filter(education="primary").count()
    secondary = readers.filter(education="secondary").count()
    higher = readers.filter(education="higher").count()
    degree = readers.filter(academic_degree=True).count()

    return {
        "primary_%": round(primary / total * 100, 2),
        "secondary_%": round(secondary / total * 100, 2),
        "higher_%": round(higher / total * 100, 2),
        "degree_%": round(degree / total * 100, 2),
    }