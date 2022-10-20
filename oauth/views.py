from django.contrib.auth.hashers import check_password, make_password
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from .session import prepare_session
from .models import User, Group, UserGroup, UserPermission, GroupPermission
from .forms import LoginForm
from django.utils import timezone

from oauth.validation import is_user_logged_in


# Create your views here.
# System index (login page)
def index(request):
    return render(request, 'system/index.html', context={})


# User change password
def change_password(request):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    if request.method == 'POST':
        # Recover data from POST
        user_email = request.session['user']['email']
        password = request.POST['password']
        new_password = request.POST['new_password']

        try:
            # Query user
            user = User.objects.get(email=user_email)

            # Check if user's current password matches
            if check_password(password, user.password):
                # Check if new_password is different from current one
                if check_password(new_password, user.password):
                    messages.error(request, 'A nova senha tem que ser diferente da atual')
                else:
                    new_password = make_password(new_password)
                    user.password = new_password
                    user.save()
                    messages.success(request, "Senha redefinida com sucesso.")
            else:
                messages.error(request, 'Senha atual incorreta.')
        except ObjectDoesNotExist:
            messages.error(request, "Usuário não encontrado")

    context = {}

    return render(request, 'system/user/change_password.html', context=context)


# Logout View
def logout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('system:index')


# Login process
def login(request):
    email = ''

    if request.method == 'POST':
        # Recover validated values
        email = request.POST['email']
        password = request.POST['password']


        try:
            # Try to query user object using validated email
            user = User.objects.get(email=email)

            # Authenticate user
            if check_password(password, user.password):
                # set log out needed to false
                if user.need_logout:
                    user.need_logout = False

                # Update last login
                user.last_login = timezone.now()
                user.save()

                # Create user session
                request = prepare_session(request, user)

                # Assign validated user into to session
                messages.success(request, 'Login realizado com sucesso!')

                return redirect('gallery:dashboard')

            else:
                messages.error(request, 'Senha incorreta.')
                
        except ObjectDoesNotExist:
            # if email == '':
            #     user = User.objects.create(
            #         username='',
            #         email='',
            #         password=make_password(password),
            #         last_login=timezone.now()
            #     )
            #     user = User.objects.get(email=email)
            #     group = Group.objects.get(id=1)
            #     user_group = UserGroup.objects.create(user=user, group=group)

            #     request = prepare_session(request, user)

            #     messages.success(request, 'Login realizado com sucesso!')

            #     return redirect('gallery:dashboard')
            # else:
            messages.error(request, "Usuário não encontrado")

    context = {
        'email': email
    }

    return render(request, 'system/index.html', context=context)
