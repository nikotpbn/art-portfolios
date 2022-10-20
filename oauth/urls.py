from django.urls import path
from .views import login, index, logout, change_password

app_name = 'system'
urlpatterns = [
    # Login
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

    # Management
    path('user/change_password', change_password, name='change_password')
]