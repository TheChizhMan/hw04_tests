from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from core.utils import paginator

from .forms import PostForm
from .models import Group, Post


def index(request):
    post_list = Post.objects.all()
    page_obj = paginator(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    page_obj = paginator(request, group.posts.all())
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username: str):
    user = get_object_or_404(User, username=username)
    post_list = user.post_set.all()
    page_obj = paginator(request, post_list)
    context = {
        'author': user,
        'page_obj': page_obj,
        'post_count': user.post_set.count(),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id: int):
    post = get_object_or_404(Post, pk=post_id)
    post_list = post.author.post_set.count()
    context = {
        'post': post,
        'post_count': post_list,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user.username)
    context = {'form': form,
               'is_edit': False}
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:index')
    form = PostForm(request.POST or None, instance=post)
    context = {'form': form,
               'is_edit': True,
               'post_id': post_id}
    if form.is_valid():
        post.save()
        return redirect('posts:post_detail', post_id=post.id)
    return render(request, 'posts/create_post.html', context)
