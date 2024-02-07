from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from men.forms import AddPostForm, UploadFileForm
from men.models import Men, Category, TagPost, UploadFiles
from men.utils import DataMixin


class AddPage(PermissionRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'men/add_page.html'
    title_page = 'Добавить статью'
    permission_required = 'men.add_men'
    

    def form_valid(self, form):
        m = form.save(commit=False)
        m.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Men
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'men/add_page.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    permission_required = 'men.change_men'


class DeletePage(DeleteView):
    model = Men
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return Men.objects.filter(slug=self.kwargs['slug']).delete()


class MenHome(DataMixin, ListView):
    template_name = 'men/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Men.published.all().select_related('cat')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


@login_required
def about(request):
    contact_list = Men.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'men/about.html', {'title': 'О сайте', 'page_obj': page_obj})


class ShowPost(DataMixin, DetailView):
    model = Men
    template_name = 'men/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Men.published, slug=self.kwargs[self.slug_url_kwarg])


class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    pass


def login(request):
    return HttpResponse('Авторизация')


class MenCategory(DataMixin, ListView):
    template_name = 'men/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Men.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.id)


class TagPostList(DataMixin, ListView):
    template_name = 'men/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Men.objects.filter(tags__slug=self.kwargs['tag_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        tag_name = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, cat_selected=None, title=f'Тег - {tag_name}')