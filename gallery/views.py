from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Exhibition, Art, Tag, ArtTag, ExhibitionArt
from .forms import CreateAndEditExhibitionForm, CreateAndEditArtForm, CreateAndEditTagForm
from django.contrib import messages
from django.core.paginator import Paginator
# Oauth
from oauth.models import User
from oauth.validation import is_user_logged_in


def dashboard(request):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    arts = Art.objects.all()
    exhibitions = Exhibition.objects.all()

    # Find arts without an exhibition relationship
    art_ids = Art.objects.values_list('id', flat=True).distinct()
    related_arts = ExhibitionArt.objects.values_list('art_id', flat=True).distinct()
    unrelated_arts = [x for x in art_ids if x not in related_arts]

    context = {
        'arts': arts.count(),
        'unrelated_arts': len(unrelated_arts),
        'exhibitions': exhibitions.count(),
    }
    return render(request, 'system/dashboard.html', context=context)


# #################################### Block Exhibition ####################################
# View to list exhibitions
def show_exhibition(request):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    exhibitions = Exhibition.objects.all().order_by('created_at').reverse()

    # Build paginator
    paginator = Paginator(exhibitions, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    # Prepare context
    context = {
        'exhibitions': exhibitions,
        'page': page,
    }
    return render(request, 'system/gallery/exhibition/show.html', context=context)


# View to add an exhibition
def add_exhibition(request):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')
    form = CreateAndEditExhibitionForm(request.POST or None, request.FILES or None)

    # Check request method
    if request.method == 'POST':
        # Validation
        if form.is_valid():
            exhibition = form.save(commit=False)
            user = User.objects.get(id=request.session['user']['id'])
            exhibition.user = user
            exhibition.save()
            messages.success(request, 'Exposição adicionada com sucesso.')
            return redirect('gallery:show_exhibition')

    context = {
        'form': form,
    }
    return render(request, 'system/gallery/exhibition/add.html', context=context)


# View to edit an exhibition
def edit_exhibition(request, id_exhibition):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    exhibition = get_object_or_404(Exhibition, id=id_exhibition)

    if request.method == 'POST':
        form = CreateAndEditExhibitionForm(request.POST, request.FILES, instance=exhibition)

        if form.is_valid():
            form.save()
            messages.success(request, "Exposição atualizada com sucesso")
            return redirect('gallery:show_exhibition')
    else:
        form = CreateAndEditExhibitionForm(instance=exhibition)

    context = {
        'exhibition': exhibition,
        'form': form,
    }

    return render(request, 'system/gallery/exhibition/edit.html', context=context)


# View to delete an exhibition
def delete_exhibition(request, id_exhibition):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    exhibition = Exhibition.objects.get(id=id_exhibition)
    exhibition_arts = ExhibitionArt.objects.filter(exhibition_id=id_exhibition)

    if exhibition_arts is not None:
        for art in exhibition_arts:
            art.delete()

    success = exhibition.delete()

    if success:
        messages.success(request, 'Exposição excluída com sucesso.')
    else:
        messages.error(request, 'Erro ao excluir Exposição.')

    return redirect('gallery:show_exhibition')


# #################################### Block Art ####################################
# View to list arts
def show_art(request):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    # Query
    arts = Art.objects.all().order_by('id').reverse()

    if request.method == 'POST':
        search_text = request.POST['search']

        if search_text.strip() != '':
            title_search = Art.objects.filter(title__icontains=search_text)
            subtitle_search = Art.objects.filter(subtitle__icontains=search_text)
            description_search = Art.objects.filter(description__icontains=search_text)

            arts_filter = title_search | subtitle_search | description_search
            arts_filter.order_by('created_at').reverse()

            if arts_filter.count() > 0:
                arts = arts_filter
            else:
                messages.error(request,
                               'não existem artes com título ou subtítulo ou descrição com esta palavra: {}'.format(
                                   search_text))

    # Build paginator
    paginator = Paginator(arts, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    # Prepare context
    context = {
        'arts': arts,
        'page': page,
    }
    return render(request, 'system/gallery/art/show.html', context=context)


# View to add an art
def add_art(request):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    # Build form
    form = CreateAndEditArtForm(request.POST or None, request.FILES or None)

    # Check request method
    if request.method == 'POST':
        # Validation
        if form.is_valid():
            art = form.save(commit=False)
            art.user = User.objects.get(id=request.session['user']['id'])
            art.save()

            messages.success(request, 'Arte adicionada com sucesso.')
            return redirect('gallery:show_art')
        else:
            msg = form.is_valid()
            messages.error(request, msg)

    context = {
        'form': form,
    }
    return render(request, 'system/gallery/art/add.html', context=context)


# View to edit an art
def edit_art(request, id_art):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    art = get_object_or_404(Art, id=id_art)

    if request.method == 'POST':
        form = CreateAndEditArtForm(request.POST, request.FILES, instance=art)

        if form.is_valid():
            form.save()
            messages.success(request, "Arte atualizada com sucesso")
            return redirect('gallery:show_art')
    else:
        form = CreateAndEditArtForm(instance=art)

    context = {
        'art': art,
        'form': form,
    }

    return render(request, 'system/gallery/art/edit.html', context=context)


# View to delete an art
def delete_art(request, id_art):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    # Query object
    art = Art.objects.get(id=id_art)

    # Find its relations with tags and arts
    art_tags = ArtTag.objects.filter()
    exhibition_arts = ExhibitionArt.objects.filter(art_id=id_art)

    # Iterare through exhibition relations and delete them
    if exhibition_arts is not None:
        for relation in exhibition_arts:
            relation.delete()

            # Update the number of arts related to an exhibition
            exhibition = Exhibition.objects.get(id=relation.exhibition.id)
            exhibition.num_works -= 1
            exhibition.save()

    # Iterare through tags relations and delete them
    if art_tags is not None:
        for tag in art_tags:
            tag.delete()

    success = art.delete()

    if success:
        messages.success(request, 'Arte excluída com sucesso.')
    else:
        messages.error(request, 'Erro ao excluir Arte.')

    return redirect('gallery:show_art')


# #################################### Block Tag ####################################
# View to list tags
def show_tag(request):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    tags = Tag.objects.all().order_by('area', 'name')

    if request.method == 'POST':
        search_text = request.POST['search']

        if search_text.strip() != '':
            id_search = Tag.objects.none()
            area_search = Tag.objects.none()
            name_search = tags.filter(name__icontains=search_text)
            try:
                cast_id = int(search_text)
                id_search = tags.filter(id__exact=cast_id)
            except ValueError:
                pass

            for tag in Tag.Options:
                if tag[1].lower() == search_text.lower():
                    area_search = tags.filter(area__exact=tag[0])

            tags_filter = id_search | name_search | area_search
            tags_filter.order_by('area', 'name')

            if tags_filter.count() > 0:
                tags = tags_filter
            else:
                messages.error(request, "Não existem tags que contenham esta palavra: {}".format(search_text))

    paginator = Paginator(tags, 9)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'tags': tags,
        'page': page,
    }
    return render(request, 'system/gallery/tag/show.html', context=context)


# View to add a tag
def add_tag(request):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    form = CreateAndEditTagForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        # Validation (check if it has a value and is not only whitespace)
        if form.is_valid():
            user = User.objects.get(id=request.session['user']['id'])
            name = form.cleaned_data.get('name')
            area = form.cleaned_data.get('area')

            t = Tag(name=name,
                    area=area,
                    user=user)
            t.save()
            messages.success(request, 'Etiqueta adicionada com sucesso.')
            return redirect('gallery:show_tag')

    context = {
        'form': form,
    }
    return render(request, 'system/gallery/tag/add.html', context=context)


# View to delete a tag
def delete_tag(request, id_tag):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    tag = Tag.objects.get(id=id_tag)
    success = tag.delete()

    if success:
        messages.success(request, 'Etiqueta excluída com sucesso.')
    else:
        messages.error(request, 'Erro ao excluir Etiqueta.')

    return redirect('gallery:show_tag')


# View to edit a tag
def edit_tag(request, id_tag):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    tag = get_object_or_404(Tag, id=id_tag)

    if request.method == 'POST':
        form = CreateAndEditTagForm(request.POST, instance=tag)

        if form.is_valid():
            form.save()
            messages.success(request, "Etiqueta atualizada com sucesso")
            return redirect('gallery:show_tag')
    else:
        form = CreateAndEditTagForm(instance=tag)

    context = {
        'tag': tag,
        'form': form,
    }

    return render(request, 'system/gallery/tag/edit.html', context=context)


# #################################### Block Art-Tag ####################################
# View to handle art tags
def art_tag(request, id_art):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    # Query art object and its related tags
    art = Art.objects.get(id=id_art)
    art_tags = ArtTag.objects.filter(art=art).values_list('tag_id', flat=True)

    # Query all tags and areas (for html accordion)
    tags = Tag.objects.all()
    areas = Tag.Options

    # Build a dictionary of all tags and areas for easy access
    area_dict = {}
    for area in areas:
        tag_list = list()
        for tag in tags:
            if area[0] == tag.area:
                tag_list.append((tag.id, tag.name))

        area_dict[area[1]] = {
            'id': area[0],
            'tag_list': tag_list,
        }

    context = {
        'art': art,
        'tags': tags,
        'art_tags': art_tags,
        'area_dict': area_dict,
    }

    return render(request, 'system/gallery/art/tag.html', context=context)


# Ajax to add or remove relations between art and tag
def handle_art_tag(request):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    id_tag = request.POST['id_tag'] or None
    id_art = request.POST['id_art'] or None

    if id_tag is not None and id_art is not None:
        art = Art.objects.get(id=id_art)
        tag = Tag.objects.get(id=id_tag)

        art_tag_query = ArtTag.objects.filter(art=art, tag=tag).first()

        if not art_tag_query:
            art_tag_object = ArtTag(art=art, tag=tag)
            art_tag_object.save()
            data = {'save': True}
        else:
            data = {'delete': True}
            art_tag_query.delete()
    else:
        data = {'save': False}

    return JsonResponse(data)


# #################################### Block Exhibition-Art ####################################
def exhibition_show_related(request, id_exhibition):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    exhibition = Exhibition.objects.get(id=id_exhibition)
    exh_arts = ExhibitionArt.objects.filter(exhibition=exhibition).order_by('exhibition__created_at').reverse()

    paginator = Paginator(exh_arts, 4)  # Show 5 arts per page.
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'exhibition': exhibition,
        'exh_arts': exh_arts,
        'page': page,
    }

    return render(request, 'system/gallery/exhibition/show_related.html', context=context)


def exhibition_add_art(request, id_exhibition):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    # Query exhibition and related arts
    exhibition = Exhibition.objects.get(id=id_exhibition)
    related = ExhibitionArt.objects.filter(exhibition=exhibition)

    # Fetch related art ids from the query set and transform into a list
    related_list = []
    for art in related:
        related_list.append(art.art_id)

    # Query all arts excluding the ones that are already related
    arts = Art.objects.all().exclude(id__in=related_list).order_by('id').reverse()

    if request.method == 'POST':
        search_text = request.POST['search']

        if search_text.strip() != '':
            title_search = arts.filter(title__icontains=search_text)
            subtitle_search = arts.filter(subtitle__icontains=search_text)
            description_search = arts.filter(description__icontains=search_text)

            arts_filter = title_search | subtitle_search | description_search
            arts_filter.order_by('created_at').reverse()

            if arts_filter.count() > 0:
                arts = arts_filter
            else:
                messages.error(request,
                               'não existem artes com título ou subtítulo ou descrição com esta palavra: {}'.format(
                                   search_text))

    # Build paginator
    paginator = Paginator(arts, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'exhibition': exhibition,
        'arts': arts,
        'page': page,
    }
    return render(request, 'system/gallery/exhibition/add_art.html', context=context)


# Relate an art with an exhibition
def exhibition_relate_art(request, id_exhibition, id_art):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    # Query objects
    exhibition = Exhibition.objects.get(id=id_exhibition)
    art = Art.objects.get(id=id_art)

    # Create and save relation, also add one, to the number of an exhibition related works.
    relation = ExhibitionArt(art=art,
                             exhibition=exhibition)
    exhibition.num_works += 1

    # Save changes
    exhibition.save()
    relation.save()

    return redirect('gallery:exhibition_add_art', id_exhibition=id_exhibition)


def exhibition_remove_art(request, id_exhibition, id_art):
    if not is_user_logged_in(request):
        messages.warning(request, 'Você precisa estar logado.')
        return redirect('system:index')

    exhibition = Exhibition.objects.get(id=id_exhibition)
    art = Art.objects.get(id=id_art)
    exh_art = ExhibitionArt.objects.get(exhibition=exhibition,
                                        art=art)
    exh_art.delete()

    exhibition.num_works -= 1
    exhibition.save()

    return redirect('gallery:exhibition_show_related', id_exhibition=exhibition.id)
