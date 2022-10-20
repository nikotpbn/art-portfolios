from django import forms


class CreateContactForm(forms.Form):
    # Name field
    name = forms.CharField(
        label='Nome: ',
        max_length=32,
        required=True,
        error_messages={
            'required': 'Você precisa inserir o seu nome.'
        }
    )

    # Last Name field
    last_name = forms.CharField(
        label='Sobrenome: ',
        max_length=32,
        required=True,
        error_messages={
            'required': 'Você precisa inserir o seu sobrenome.'
        }
    )

    # Email field
    from_email = forms.EmailField(
        label='Email: ',
        max_length=64,
        required=True,
        error_messages= {
            'required': 'Você precisa inserir o seu email'
        }
    )

    # Topic of the message
    subject = forms.CharField(
        label='Assunto: ',
        max_length=256,
        required=True,
        error_messages={
            'required': 'Você precisa inserir um assunto.'
        }
    )

    # Subject / Body of the message
    message = forms.CharField(
        label='Corpo: ',
        widget=forms.Textarea,
        max_length=256,
        required=True,
        error_messages={
            'required': 'Você precisa preencher o corpo da mensagem.'
        }
    )

    class Meta:
        fields = [
            'name',
            'last_name',
            'from_email',
            'subject',
            'message',
        ]
