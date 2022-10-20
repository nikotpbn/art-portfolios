from django.urls import path
from .views import show_exhibition, add_exhibition, edit_exhibition, delete_exhibition, \
    exhibition_show_related, exhibition_add_art, exhibition_relate_art, exhibition_remove_art, \
    show_art, add_art, edit_art, delete_art, art_tag, handle_art_tag, \
    show_tag, add_tag, edit_tag,  delete_tag, \
    dashboard

app_name = 'gallery'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),

    # Exhibition
    path('show/exhibition', show_exhibition, name='show_exhibition'),
    path('add/exhibition', add_exhibition, name='add_exhibition'),
    path('edit/exhibition/<int:id_exhibition>', edit_exhibition, name='edit_exhibition'),
    path('delete/exhibition/<int:id_exhibition>', delete_exhibition, name='delete_exhibition'),
    path('show/exhibition/art/<int:id_exhibition>', exhibition_show_related, name='exhibition_show_related'),
    path('add/exhibition/art/<int:id_exhibition>', exhibition_add_art, name='exhibition_add_art'),
    path('relate/exhibition/art/<int:id_exhibition>/<int:id_art>', exhibition_relate_art, name='exhibition_relate_art'),
    path('remove/exhibition/art/<int:id_exhibition>/<int:id_art>', exhibition_remove_art, name='exhibition_remove_art'),

    # Art
    path('show/art', show_art, name='show_art'),
    path('add/art', add_art, name='add_art'),
    path('edit/art/<int:id_art>', edit_art, name='edit_art'),
    path('delete/art/<int:id_art>', delete_art, name='delete_art'),
    path('art/tag/<int:id_art>', art_tag, name='art_tag'),
    path('handle/art/tag/', handle_art_tag, name='handle_art_tag'),

    # Tags
    path('show/tag', show_tag, name='show_tag'),
    path('add/tag', add_tag, name='add_tag'),
    path('edit/tag/<int:id_tag>', edit_tag, name='edit_tag'),
    path('delete/tag/<int:id_tag>', delete_tag, name='delete_tag'),
]
