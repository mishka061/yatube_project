#from django.contrib import admin
from django.urls import path, include
from . import views
#from posts.views import *

urlpatterns = [
    path('', views.index),
    path('posts/', views.group_posts),
    #path('group/<slug:slug>/', views.group_posts),

    #   path('admin/', admin.site.urls),
]
