from django.contrib import admin

from .models import Post, Group

# Перечисляем поля, которые должны отображаться в админке
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    list_editable = ('group',)  # изменяет поле group в любом посте
    search_fields = ('text',)  # Добавляет интерфейс для поиска по тексту постов
    list_filter = ('pub_date',)  # Добавляет возможность фильтрации по дате
    empty_value_display = '-пусто-'  # Это свойство для всех колонок: где пусто — там будет эта строка
# При регистрации модели Post источником конфигурации для неё назначаем
# класс PostAdmin
admin.site.register(Post, PostAdmin)
#Регистрация даст возможность создавать новые группы через админ-зону.
admin.site.register(Group)
