from .utils import is_airport_admin


def airport_admin_context(request):
    """
    Добавляет is_admin в контекст всех шаблонов
    """
    return {
        'is_admin': is_airport_admin(request.user) if request.user.is_authenticated else False,
    }
