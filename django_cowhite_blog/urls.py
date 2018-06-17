from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^blog/$', views.BlogPostListView.as_view(), name="blog-post-list"),
    url(r'^blog/(?P<slug>[\w-]+)/$', views.BlogPostView.as_view(), name="blog-post"),
]
