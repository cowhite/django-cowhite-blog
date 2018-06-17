from django.shortcuts import render, get_object_or_404
from django.views import generic as generic_views

from .models import *


class BlogPostListView(generic_views.TemplateView):
    template_name = "django_cowhite_blog/blog_post_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BlogPostListView, self).get_context_data(*args, **kwargs)
        context['blog_posts'] = BlogPost.objects.filter(status=PUBLISH_STATUS_CHOICE_PUBLISHED)
        return context


class BlogPostView(generic_views.TemplateView):
    template_name = "django_cowhite_blog/blog_post.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BlogPostView, self).get_context_data(*args, **kwargs)
        # context['blog_post'] = BlogPost.objects.get(status=PUBLISH_STATUS_CHOICE_PUBLISHED)
        context['blog_post'] = get_object_or_404(BlogPost, slug=kwargs['slug'])
        return context

