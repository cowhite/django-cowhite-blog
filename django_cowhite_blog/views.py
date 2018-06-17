from django.shortcuts import render, get_object_or_404
from django.views import generic as generic_views
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from .models import *


class BlogPostListView(generic_views.TemplateView):
    template_name = "django_cowhite_blog/blog_post_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BlogPostListView, self).get_context_data(*args, **kwargs)
        context['blog_posts'] = BlogPost.objects.filter(status=PUBLISH_STATUS_CHOICE_PUBLISHED)

        blog_posts = BlogPost.objects.filter(status=PUBLISH_STATUS_CHOICE_PUBLISHED)

        paginator = Paginator(blog_posts, 10) # Show 25 contacts per page

        page = self.request.GET.get('page')

        try:
            blog_posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            blog_posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            blog_posts = paginator.page(paginator.num_pages)

        context['blog_posts'] = blog_posts
        return context


class BlogPostView(generic_views.TemplateView):
    template_name = "django_cowhite_blog/blog_post.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BlogPostView, self).get_context_data(*args, **kwargs)
        context['blog_post'] = get_object_or_404(BlogPost, slug=kwargs['slug'])
        return context

