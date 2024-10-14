from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField

# Класс PublishedManager наследуется от models.Manager и переопределяет метод get_queryset.
# Он возвращает queryset, отфильтрованный по статусу публикации (только опубликованные записи).
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Men.Status.PUBLISHED)

# Класс Men наследуется от models.Model и определяет модель для хранения информации о мужчинах.
class Men(models.Model):
    # Вложенный класс Status определяет статусы записей (черновик, опубликовано).
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    # Поле title хранит заголовок записи.
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    
    # Поле slug автоматически генерируется на основе поля title и содержит URL-дружелюбный идентификатор.
    slug = AutoSlugField(populate_from='title', unique=True, verbose_name='URL', validators=[
                               MinLengthValidator(5, message='Слишком короткий слаг.'),
                               MaxLengthValidator(100),
                           ])
    
    # Поле photo хранит фотографию записи.
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None,
                              blank=True, null=True, verbose_name='Фото')
    
    # Поле content хранит текст статьи.
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    
    # Поле time_create автоматически устанавливается при создании записи.
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    
    # Поле time_update автоматически обновляется при сохранении записи.
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    
    # Поле is_published хранит статус публикации записи.
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name='Публикация')
    
    # Поле cat является внешним ключом на модель Category.
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    
    # Поле tags является связью многие-ко-многим с моделью TagPost.
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Тэги')
    
    # Поле wife является связью один-к-одному с моделью Wife.
    wife = models.OneToOneField('Wife', on_delete=models.SET_NULL, null=True, blank=True, related_name='mean',
                                verbose_name='Супруга')
    
    # Поле author является внешним ключом на модель пользователя.
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               related_name='posts', null=True, default=None)
    
    # Объекты модели управляются стандартным менеджером.
    objects = models.Manager()
    
    # Объекты модели, отфильтрованные по статусу публикации, управляются менеджером PublishedManager.
    published = PublishedManager()

    # Метод __str__ возвращает строковое представление объекта.
    def __str__(self):
        return self.title

    # Вложенный класс Meta содержит метаданные модели.
    class Meta:
        verbose_name = 'Известные мужчины'
        verbose_name_plural = 'Известные мужчины'
        ordering = ['time_create']
        indexes = [
            models.Index(fields=['time_create'])
        ]

    # Метод get_absolute_url возвращает URL для доступа к объекту.
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # Метод save переопределяет стандартный метод сохранения объекта.
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


# Класс Category наследуется от models.Model и определяет модель для хранения категорий.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')

    # Метод __str__ возвращает строковое представление объекта.
    def __str__(self):
        return self.name

    # Метод get_absolute_url возвращает URL для доступа к объекту.
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    # Вложенный класс Meta содержит метаданные модели.
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# Класс TagPost наследуется от models.Model и определяет модель для хранения тэгов.
class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    # Вложенный класс Meta содержит метаданные модели.
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    # Метод __str__ возвращает строковое представление объекта.
    def __str__(self):
        return self.tag

    # Метод get_absolute_url возвращает URL для доступа к объекту.
    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


# Класс Wife наследуется от models.Model и определяет модель для хранения информации о супругах.
class Wife(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    # Вложенный класс Meta содержит метаданные модели.
    class Meta:
        verbose_name = 'Супругу'
        verbose_name_plural = 'Супруги'

    # Метод __str__ возвращает строковое представление объекта.
    def __str__(self):
        return self.name


# Класс UploadFiles наследуется от models.Model и определяет модель для хранения загруженных файлов.
class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')


# Класс Comment наследуется от models.Model и определяет модель для хранения комментариев.
class Comment(models.Model):
    post = models.ForeignKey(Men, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.author.username} к {self.post.title}'