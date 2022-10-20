from django.db import models
from oauth.models import User
from django.utils import timezone
import uuid
from django.conf import settings


def generate_exhibition_image_hash(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{}.{}".format(uuid.uuid4().hex, ext)
    upload_path = f'{settings.UPLOAD_ROOT}/cover/' + filename

    return upload_path


def generate_art_image_hash(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{}.{}".format(uuid.uuid4().hex, ext)
    upload_path = f'{settings.UPLOAD_ROOT}/drawings/' + filename

    return upload_path


# Create your models here.
class Exhibition(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256, null=False)
    cover = models.FileField(upload_to=generate_exhibition_image_hash)
    num_works = models.IntegerField(null=False, default=0)
    created_at = models.DateField(null=False, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = 'gallery_exhibition'


class Art(models.Model):
    Options = [
        (1, 'Drawing'),
        (2, 'Painting'),
        (3, 'Digital'),
        (4, 'Tatoo'),
        (5, 'Photo')
    ]


    # Options = [
    #     (1, 'Desenho'),
    #     (2, 'Pintura'),
    #     (3, 'Escultura'),
    #     (4, 'Cerâmica'),
    #     (5, 'Digital'),
    #     (6, 'Fotografia'),
    #     (7, 'Tatuagem'),
    # ]

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256, null=False)
    subtitle = models.CharField(max_length=256, null=True)
    description = models.TextField(max_length=512, null=True)
    image = models.FileField(upload_to=generate_art_image_hash)
    type = models.IntegerField(choices=Options, null=False)
    created_at = models.DateField(null=False, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = 'gallery_art'


class ExhibitionArt(models.Model):
    id = models.IntegerField(primary_key=True)
    exhibition = models.ForeignKey(Exhibition, on_delete=models.PROTECT, null=False)
    art = models.ForeignKey(Art, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = 'gallery_exhibition_art'


class Tag(models.Model):
    Options = [
        (1, 'Materials'),
        (2, 'Inspiration'),
        (3, 'Penciler'),
        (4, 'Inker'),
        (5, 'Color')
    ]

    # Options = [
    #     (1, 'Cor'),
    #     (2, 'Tinta'),
    #     (3, 'Lápis'),
    #     (4, 'Nanquim'),
    #     (5, 'Papel'),
    #     (6, 'Quadro'),
    #     (7, 'Estilo'),
    #     (8, 'Materials')
    # ]

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False, unique=True)
    area = models.IntegerField(choices=Options, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    created_at = models.DateField(null=False, default=timezone.now)

    class Meta:
        db_table = 'gallery_tag'


class ArtTag(models.Model):
    id = models.IntegerField(primary_key=True)
    art = models.ForeignKey(Art, on_delete=models.PROTECT, null=False)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = 'gallery_art_tag'
