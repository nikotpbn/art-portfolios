from .models import UserGroup


# Function to prepare the sessions
def prepare_session(request, database_user):
    group = UserGroup.objects.get(user=database_user).group

    request.session['user'] = {
        'id': database_user.id,
        'name': database_user.name,
        'username': database_user.username,
        'email': database_user.email,
        'group_id': group.id,
        'group': group.name,
        'need_logout': database_user.need_logout,
    }

    if database_user.image:
        request.session['user']['image'] = database_user.image.url
    else:
        request.session['user']['image'] = 'https://storage.googleapis.com/diogo-ferreira-portfolio.appspot.com/static/system/images/d-avatar.jpg'

    return request
