from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def staff_required(view_func):
    """Декоратор для проверки прав администратора"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Требуются права администратора.')
            return redirect('tour_list')
    return _wrapped_view