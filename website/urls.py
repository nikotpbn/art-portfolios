from django.urls import path
from .views import index, exhibition, gallery, contact, about

app_name = 'website'

urlpatterns = [
    # Website
    path('', index, name='index'),
    path('galerias', exhibition, name='exhibition'),
    path('galeria/<int:id_exhibition>', gallery, name='gallery'),
    path('contato', contact, name='contact'),
    path('about', about, name='about'),
]
