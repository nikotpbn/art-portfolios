from django import forms
from .models import Exhibition, Art, Tag


class CreateAndEditExhibitionForm(forms.ModelForm):
    # Name field
    name = forms.CharField(
        label='Nome: ',
        max_length=256,
        required=True,
        error_messages={
            'required': 'Você precisa inserir o nome da galeria.'
        }
    )

    cover = forms.FileField(
        label='Selecione a imagem de capa...',
        required=True,
        error_messages={
            'required': 'Você precisa selecionar uma imagem de capa'
        }
    )

    user = forms.HiddenInput()

    # This class sets the fields that should be in the views.
    class Meta:
        model = Exhibition
        fields = [
            'name',
            'cover',
        ]


class CreateAndEditArtForm(forms.ModelForm):
    title = forms.CharField(
        label='Título: ',
        max_length=256,
        required=True,
        error_messages={
            'required': 'Você precisa inserir o nome da galeria.'
        }
    )

    subtitle = forms.CharField(
        label='Subtítulo: ',
        max_length=256,
        required=False,
    )

    description = forms.CharField(
        label='Descrição: ',
        required=False,
        widget=forms.Textarea
    )

    image = forms.FileField(
        label='Selecione a imagem...',
        required=True,
        error_messages={
            'required': 'Você precisa selecionar uma imagem'
        }
    )

    type = forms.CharField(
        label='Tipo de Arte:',
        required=True,
        widget=forms.Select(choices=Art.Options),
        error_messages={
            'required': 'Você precisa informar o tipo de arte'
        }
    )

    # This class sets the fields that should be in the views.
    class Meta:
        model = Art
        fields = [
            'title',
            'subtitle',
            'description',
            'image',
            'type',
        ]


class CreateAndEditTagForm(forms.ModelForm):
    name = forms.CharField(
        label='Nome: ',
        max_length=256,
        required=True,
        error_messages={
            'required': 'Você precisa inserir o nome da etiqueta.'
        }
    )

    area = forms.CharField(
        label='Area:',
        required=True,
        widget=forms.Select(choices=Tag.Options),
        error_messages={
            'required': 'Você precisa informar a area da etiqueta'
        }
    )

    # This class sets the fields that should be in the views.
    class Meta:
        model = Tag
        fields = [
            'name',
            'area',
        ]
