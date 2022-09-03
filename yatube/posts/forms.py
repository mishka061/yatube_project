from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = {
            'text': 'Текст подсказки',
            'group': 'Группа'
        }
        labels = {
            'group': 'Группа',
            'text': 'Текст подсказки'
        }


class PostCreateForm:
    pass
