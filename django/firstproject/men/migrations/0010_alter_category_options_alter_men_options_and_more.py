# Generated by Django 4.2.7 on 2024-01-11 11:22

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('men', '0009_wife_m_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='men',
            options={'ordering': ['time_create'], 'verbose_name': 'Известные мужчины', 'verbose_name_plural': 'Известные мужчины'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='Слаг'),
        ),
        migrations.AlterField(
            model_name='men',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='men.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='men',
            name='content',
            field=models.TextField(blank=True, verbose_name='Текст статьи'),
        ),
        migrations.AlterField(
            model_name='men',
            name='is_published',
            field=models.BooleanField(choices=[(False, 'Черновик'), (True, 'Опубликовано')], default=0, verbose_name='Публикация'),
        ),
        migrations.AlterField(
            model_name='men',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, validators=[django.core.validators.MinLengthValidator(5, message='Слишком короткий слаг.'), django.core.validators.MaxLengthValidator(100)], verbose_name='Слаг'),
        ),
        migrations.AlterField(
            model_name='men',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='men.tagpost', verbose_name='Тэги'),
        ),
        migrations.AlterField(
            model_name='men',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='men',
            name='time_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Время обновления'),
        ),
        migrations.AlterField(
            model_name='men',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='men',
            name='wife',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mean', to='men.wife', verbose_name='Супруга'),
        ),
    ]
