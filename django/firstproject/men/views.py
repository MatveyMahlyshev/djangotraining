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

# Класс AddPage наследуется от PermissionRequiredMixin, DataMixin и CreateView.
# Он позволяет добавлять новые записи в модель Men, если у пользователя есть соответствующее разрешение.
class AddPage(PermissionRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm  # Указываем форму, которая будет использоваться для создания записи.
    template_name = 'men/add_page.html'  # Указываем шаблон, который будет использоваться для отображения формы.
    title_page = 'Добавить статью'  # Указываем заголовок страницы.
    permission_required = 'men.add_men'  # Указываем разрешение, необходимое для доступа к этому представлению.
    
    # Метод form_valid выполняется, если форма валидна.
    def form_valid(self, form):
        m = form.save(commit=False)  # Создаем объект модели, но не сохраняем его в базу данных.
        m.author = self.request.user  # Устанавливаем автора записи как текущего пользователя.
        return super().form_valid(form)  # Сохраняем объект в базу данных и выполняем стандартный метод form_valid.

# Класс UpdatePage наследуется от PermissionRequiredMixin, DataMixin и UpdateView.
# Он позволяет редактировать существующие записи в модели Men, если у пользователя есть соответствующее разрешение.
class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Men  # Указываем модель, которую будем редактировать.
    fields = ['title', 'content', 'photo', 'is_published', 'cat']  # Указываем поля, которые можно редактировать.
    template_name = 'men/add_page.html'  # Указываем шаблон, который будет использоваться для отображения формы.
    success_url = reverse_lazy('home')  # Указываем URL, на который будет перенаправлен пользователь после успешного редактирования.
    title_page = 'Редактирование статьи'  # Указываем заголовок страницы.
    permission_required = 'men.change_men'  # Указываем разрешение, необходимое для доступа к этому представлению.

# Класс DeletePage наследуется от DeleteView.
# Он позволяет удалять записи из модели Men.
class DeletePage(DeleteView):
    model = Men  # Указываем модель, из которой будем удалять записи.
    success_url = reverse_lazy('home')  # Указываем URL, на который будет перенаправлен пользователь после успешного удаления.

    # Метод get_object возвращает объект, который будет удален.
    def get_object(self, queryset=None):
        return Men.objects.filter(slug=self.kwargs['slug']).delete()

# Класс MenHome наследуется от DataMixin и ListView.
# Он отображает список всех опубликованных записей.
class MenHome(DataMixin, ListView):
    template_name = 'men/index.html'  # Указываем шаблон, который будет использоваться для отображения списка записей.
    context_object_name = 'posts'  # Указываем имя переменной контекста, которая будет содержать список записей.
    title_page = 'Главная страница'  # Указываем заголовок страницы.
    cat_selected = 0  # Указываем, что выбрана категория с ID 0 (все категории).

    # Метод get_queryset возвращает queryset с опубликованными записями.
    def get_queryset(self):
        return Men.published.all().select_related('cat')

# Функция page_not_found обрабатывает ошибку 404 (страница не найдена).
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

# Функция about отображает страницу "О сайте".
@login_required  # Декоратор login_required требует, чтобы пользователь был авторизован для доступа к этой странице.
def about(request):
    contact_list = Men.published.all()  # Получаем все опубликованные записи.
    paginator = Paginator(contact_list, 3)  # Создаем объект Paginator для разбиения списка записей на страницы.

    page_number = request.GET.get('page')  # Получаем номер текущей страницы из GET-параметра.
    page_obj = paginator.get_page(page_number)  # Получаем объект страницы.

    return render(request, 'men/about.html', {'title': 'О сайте', 'page_obj': page_obj})  # Рендерим шаблон с контекстом.

# Класс ShowPost наследуется от DataMixin и DetailView.
# Он отображает детали конкретной записи.
class ShowPost(DataMixin, DetailView):
    model = Men  # Указываем модель, из которой будем получать запись.
    template_name = 'men/post.html'  # Указываем шаблон, который будет использоваться для отображения записи.
    slug_url_kwarg = 'post_slug'  # Указываем имя параметра URL, который содержит слаг записи.
    context_object_name = 'post'  # Указываем имя переменной контекста, которая будет содержать запись.

    # Метод get_context_data добавляет дополнительные данные в контекст.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user == context['post'].author  # Проверяем, является ли текущий пользователь автором записи.
        return self.get_mixin_context(context, title=context['post'].title)  # Возвращаем обновленный контекст.

    # Метод get_object возвращает объект записи.
    def get_object(self, queryset=None):
        return get_object_or_404(Men.published, slug=self.kwargs[self.slug_url_kwarg])

# Класс ContactFormView наследуется от LoginRequiredMixin, DataMixin и FormView.
# Он отображает форму обратной связи.
class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    pass

# Функция login отображает страницу авторизации.
def login(request):
    return HttpResponse('Авторизация')

# Класс MenCategory наследуется от DataMixin и ListView.
# Он отображает список записей, относящихся к определенной категории.
class MenCategory(DataMixin, ListView):
    template_name = 'men/index.html'  # Указываем шаблон, который будет использоваться для отображения списка записей.
    context_object_name = 'posts'  # Указываем имя переменной контекста, которая будет содержать список записей.

    # Метод get_queryset возвращает queryset с записями, относящимися к определенной категории.
    def get_queryset(self):
        return Men.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    # Метод get_context_data добавляет дополнительные данные в контекст.
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat  # Получаем категорию первой записи в списке.
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.id)  # Возвращаем обновленный контекст.

# Класс TagPostList наследуется от DataMixin и ListView.
# Он отображает список записей, относящихся к определенному тегу.
class TagPostList(DataMixin, ListView):
    template_name = 'men/index.html'  # Указываем шаблон, который будет использоваться для отображения списка записей.
    context_object_name = 'posts'  # Указываем имя переменной контекста, которая будет содержать список записей.
    allow_empty = False  # Указываем, что отображение пустого списка запрещено.

    # Метод get_queryset возвращает queryset с записями, относящимися к определенному тегу.
    def get_queryset(self):
        return Men.objects.filter(tags__slug=self.kwargs['tag_slug'])

    # Метод get_context_data добавляет дополнительные данные в контекст.
    def get_context_data(self, *, object_list=None, **kwargs):
        tag_name = TagPost.objects.get(slug=self.kwargs['tag_slug'])  # Получаем тег по слагу.
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, cat_selected=None, title=f'Тег - {tag_name}')  # Возвращаем обновленный контекст.