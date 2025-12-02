from .models import AirportAdminProfile


def is_airport_admin(user):
    """
    Проверяет, является ли пользователь администратором аэропорта

    Args:
        user: Объект пользователя Django

    Returns:
        bool: True если пользователь является администратором, False иначе
    """
    if not user or not user.is_authenticated:
        return False

    try:
        profile = user.airport_admin_profile
        return profile.is_airport_admin
    except AirportAdminProfile.DoesNotExist:
        return False
