from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {
            'text': 'Текст подсказки',
            'group': 'Группа',
            'image': 'Картинка'
        }
        labels = {
            'group': 'Группа',
            'text': 'Текст подсказки'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {
            'text': 'Текст подсказки'
        }
        labels = {'text': 'Комментарий'}
        help_texts = {
            'text': 'Комментарий к посту'
        }


class PostCreateForm:
    pass
