def is_user_logged_in(request):
    if 'user' not in request.session:
        return False
    else:
        return True
