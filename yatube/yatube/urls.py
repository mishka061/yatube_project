
# главная страница
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('posts.urls', namespace='posts')),
    path('admin/', admin.site.urls),
    # джанго сначала ищет совпадения  path по  urls приложения posts
    # если не найдет,то ищет здесь,в головном сайте

]
