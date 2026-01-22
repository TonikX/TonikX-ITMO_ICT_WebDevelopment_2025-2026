# utils.py
from django.shortcuts import redirect

def redirect_user_by_role(user):
    """Essential function that redirects the user to the homework page."""
    if user.is_superuser or user.is_staff:
        return redirect('/admin/')
    elif getattr(user, 'role', None) == "student":
        return redirect('student_profile')
    elif getattr(user, 'role', None) == "teacher":
        return redirect('teacher_profile')
    return redirect('login')