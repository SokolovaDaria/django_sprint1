from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post
from .utils import get_published_posts


def index(request):
    post_list = get_published_posts()[:5]
    return render(request, 'blog/index.html', {'post_list': post_list})


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    post_list = get_published_posts().filter(category=category)
    return render(request, 'blog/category.html',
                  {'category': category, 'post_list': post_list})


def post_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    if (post.pub_date > timezone.now() or not post.is_published
            or not post.category.is_published):
        raise Http404("Страница не найдена")
    return render(request, 'blog/detail.html', {'post': post})
