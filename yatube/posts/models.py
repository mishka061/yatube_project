from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название группы',
        help_text='Выберите группу'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес группы',
        help_text='Выберите адрес группы'
    )
    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Выберите описание группы'
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    objects = None
    text = models.TextField(
        max_length=200,
        verbose_name='Текст поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор поста'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        verbose_name='Группа поста',
        related_name='posts',
        blank=True,
        null=True,
        help_text='Выберите группу'
    )

    class Meta:
        verbose_name = 'Пост'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]
