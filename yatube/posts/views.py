from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CreationForm
from .models import Group, Post
from .utils import paginate_page


def index(request):
    page_obj = paginate_page(request, Post.objects.all())
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    page_obj = paginate_page(request, group.posts.all())
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context=context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    page_obj = paginate_page(request, author.posts.all())
    context = {
        'author': author,
        'page_obj': page_obj,
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
    form = CreationForm(request.POST)
    if form.is_valid():
        Post.objects.create(**form.cleaned_data, author=request.user)
        return redirect('posts:profile', request.user.username)
    context = {
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('posts:post_detail', post_id)

    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            Post.objects.filter(id=post_id).update(
                **form.cleaned_data,
            )
            return redirect('posts:post_detail', post_id)
    else:
        form = CreationForm(instance=post)

    context = {
        'form': form,
        'is_edit': True,
        'post_id': post_id
    }

    return render(request, 'posts/create_post.html', context)


def self_profile(request):
    return redirect('posts:profile', request.user.username)
