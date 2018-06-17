from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from .models import *

import datetime


class Common(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create_user(
            username= "user1", password= "a",
            email= "user1@example.com")
        for x in range(1, 23):
            BlogPost.objects.create(
                title='This is blog post - %s' % x, content='<h1>Blog content</h1>',
                author=self.user1, status='P')


class BlogPostTestCase(Common):
    def test_blog_post_list(self):
        url = reverse("django-cowhite-blog:blog-post-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['blog_posts'].paginator.num_pages, 3)

    def test_blog_post(self):
        first_blog = BlogPost.objects.first()
        url = reverse("django-cowhite-blog:blog-post", args=[first_blog.slug])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['blog_post'].title, first_blog.title)


