import django.http
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, QueryDict, HttpResponseRedirect
from datetime import datetime
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from men.forms import AddPostForm
from men.models import Men, Category, TagPost

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'}
]

data_db = [
    {'id': 1, 'title': 'Криштиану Роналду', 'content': '''Криштиану Роналду родился 5 февраля 1985 года в португальском городе Фуншал на острове Мадейра в простой небогатой семье. Мать Роналду — Мария Долореш была поваром, а отец — садовником. Криштиану оказался четвертым ребенком в семье — у Роналду есть старший брат Угу и две старшие сестры Эльма и Лилиана Катя.
Португалец начал играть в футбол в три года. В шесть лет Роналду пошел в школу и попал в академию «Андориньи», где подрабатывал отец, подготавливая форму к играм. С учебой у португальца не ладилось — он получал хорошие оценки, но регулярно нарушал дисциплину. В 14 лет Роналду исключили из школы за то, что он бросил в учителя стулом.''',
     'is_published': True},
    {'id': 2, 'title': 'Джонни Депп', 'content': 'Биография Джонни Деппа', 'is_published': True},
    {'id': 3, 'title': 'Леонардо Ди Каприо', 'content': 'Биография Леонардо Ди Каприо', 'is_published': False},
]


def index(request):
    posts = Men.published.all().select_related('cat')

    data = {'title': 'Главная страница',
            'menu': menu,
            'posts': posts,
            'cat_selected': 0,
            }
    return render(request, 'men/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def about(request):
    return render(request, 'men/about.html', {'title': 'О сайте', 'menu': menu})


def show_post(request, post_slug):
    post = get_object_or_404(Men, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1
    }
    return render(request, 'men/post.html', data)


def add_page(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            try:
                Men.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()
    data = {
        'menu': menu,
        'title': 'Добавление статьи',
        'form': form
    }
    return render(request, 'men/add_page.html', context=data)


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Men.published.filter(cat_id=category.pk).select_related('cat')

    data = {'title': f'Рубрика: {category.name}',
            'menu': menu,
            'posts': posts,
            'cat_selected': category,
            }
    return render(request, 'men/index.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Men.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,

    }
    return render(request, 'men/index.html', context=data)
