# Generated by Django 3.2.13 on 2022-05-14 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20220514_0737'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('text', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Текст')),
                ('image', models.FileField(blank=True, null=True, upload_to='', verbose_name='Картинка')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'ordering': ['-datetime'],
            },
        ),
    ]
