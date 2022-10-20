from django.shortcuts import render
from gallery.models import Exhibition, ExhibitionArt, Art, ArtTag
from .forms import CreateContactForm
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.core import mail
from django.contrib import messages


def index(request):
    most_recent_arts = Art.objects.all().order_by('-created_at')[:12]

    context = {'most_recent_arts': most_recent_arts, }
    return render(request, 'website/index.html', context=context)

def about(request):
    return render(request, 'website/about.html')

def exhibition(request):
    exhibitions = Exhibition.objects.all()
    context = {'galleries': exhibitions, }
    return render(request, 'website/galleries.html', context=context)


def gallery(request, id_exhibition):
    exhibition = Exhibition.objects.get(id=id_exhibition)
    related = ExhibitionArt.objects.filter(exhibition=exhibition)

    context = {
        'exhibition': exhibition,
        'related': related,
    }
    return render(request, 'website/gallery.html', context=context)


def contact(request):
    form = CreateContactForm()

    if request.method == 'POST':
        form = CreateContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            last_name = form.cleaned_data.get('last_name')
            sender = form.cleaned_data.get('from_email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            recipients = ['nikobeltrao@hotmail.com']

            print(f'Name: {name} - Last Name: {last_name}')
            print(f'email: {sender}')
            print(f'subject: {subject}')
            print(f'message: {message}')

        else:
            print('Formulário inválido')

    context = {
        'form': form,
    }
    return render(request, 'website/contact.html', context=context)
