# Generated by Django 4.2.7 on 2023-11-21 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('men', '0003_alter_men_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='men',
            name='is_published',
            field=models.BooleanField(choices=[(0, 'Черновик'), (1, 'Опубликовано')], default=0),
        ),
    ]
