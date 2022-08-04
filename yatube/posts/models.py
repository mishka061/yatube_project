
from django.db import models
# Из модуля auth импортируем функцию get_user_model
from django.contrib.auth import get_user_model

User = get_user_model()

#модель для сообществ
class Group(models.Model):
    title = models.CharField(max_length=200) # Название группы содержит максимум 200 символов
    slug = models.SlugField(max_length=200) # Уникальный адрес группы содержит максимум 200 символов
    description = models.CharField(max_length=200)#описание сообщества,которое отображается на странице

    def __str__(self):
        return self.title

class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    # при добавлении новой записи ссылается на сообщество Group
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,#удаление модели
        related_name='posts',
        blank=True,
        null=True,

    )

