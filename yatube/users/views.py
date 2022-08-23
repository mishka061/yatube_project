from django.views.generic import CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


def only_user_view(request):
    if not request.username.is_authenticated:
        return redirect('/auth/login/')
