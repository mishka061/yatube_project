from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .models import Post, Group, User
from django.shortcuts import redirect


POST_PER_PAGE = 10


def get_page(request, post_list):
    paginator = Paginator(post_list, POST_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all().select_related('author', 'group')
    page_obj = get_page(request, posts)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.all().select_related('author', 'group')
    page_obj = get_page(request, posts)
    context = {
        'page_obj': page_obj,
        'group': group,
        'posts': posts
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    page_obj = get_page(request, posts)
    context = {
        'page_obj': page_obj,
        'username': author,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user

        post.save()
        return redirect('posts:profile', request.user)
    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    return render(
        request,
        'posts/post_create.html',
        {'form': form,
         'is_edit': True}
    )
