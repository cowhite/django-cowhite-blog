from django.db import models
from django.utils.text import slugify


PUBLISH_STATUS_CHOICE_DRAFT = 'D'
PUBLISH_STATUS_CHOICE_PUBLISHED = 'P'

PUBLISH_STATUS_CHOICES = (
    (PUBLISH_STATUS_CHOICE_DRAFT, 'Draft'),
    (PUBLISH_STATUS_CHOICE_PUBLISHED, 'Published'),
)


class DateTimeBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def generate_unique_slug(self):
        title = self.title
        if self.slug:
            return self.slug
        slug_initial = slugify(self.title)
        slug = slug_initial
        model = self.__class__
        i = 1
        while True:
            try:
                model.objects.get(slug=slug)
                slug = "%s%s" % (slug_initial, i)
                i += 1
                continue
            except model.DoesNotExist:
                break
        return slug




class Category(DateTimeBase):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=500, unique=True)



class BlogPost(DateTimeBase):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True, blank=True)
    content = models.TextField()
    categories = models.ManyToManyField(Category, blank=True)
    status = models.CharField(
        choices=PUBLISH_STATUS_CHOICES, max_length=1,
        default=PUBLISH_STATUS_CHOICE_DRAFT)
    published_date = models.DateTimeField(null=True, blank=True)
    allow_comments = models.BooleanField(default=True)
    related_posts = models.ManyToManyField('BlogPost', blank=True)

    # SEO
    seo_title = models.CharField(max_length=500,
        help_text='Optional. This title is inserted in HTML Title tag. If not filled, blog title will be used.',
        blank=True)
    seo_description = models.TextField(null=True, blank=True,
        help_text='Optional. This description is inserted in HTML meta description tag.'
        'If not filled, the first paragraph from the content will be inserted here.')
    seo_keywords = models.TextField(null=True, blank=True,
        help_text='Optional. This is not auto generated. The filled content will be'
        'inserted in meta keywords tag')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        if not self.seo_title:
            self.seo_title = self.title
        if not self.seo_description:
            self.seo_description = "%s..." % self.content.split("\n")[0][:250]
        super(BlogPost, self).save(*args, **kwargs)


