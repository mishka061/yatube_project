from django.shortcuts import render
from django.http import HttpResponse

# posts_dict = {
#   'photo': 'пост о фотографиях',
#   'video': 'пост о видео',
# }


def index(request):
    return HttpResponse('Главная страница')


def group_posts(request):
    return HttpResponse('Посты сообщества')
