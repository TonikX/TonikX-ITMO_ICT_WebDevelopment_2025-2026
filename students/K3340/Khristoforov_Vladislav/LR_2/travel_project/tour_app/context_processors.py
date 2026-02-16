def user_perms(request):
    return {
        'user_is_staff': request.user.is_staff if request.user.is_authenticated else False,
    }