from django import template

register = template.Library()

@register.filter
def filter_submissions(submissions, student):
    return [s for s in submissions if s.student == student]

@register.filter
def avg_grade(submissions):
    if not submissions:
        return 0
    grades = [s.grade for s in submissions if s.grade > 0]
    if not grades:
        return 0
    return sum(grades) / len(grades)