from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.

    #'wlasny menager filtruje tylko opublikowane
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (('draft','Draft'),('published','Published'),)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

    tags = TaggableManager()  # dodaje meneger tagow
    'managery'
    objects = models.Manager()  # manager domyślny.
    published = PublishedManager()  # Własny menedżer.


    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title

    'tworzy sciezke  ze zmiennymi konkretnego posta z get absolute do samego siebie czyli do post'
    def get_absolute_url(self):
        return reverse('blog_2:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])

class Comment(models.Model):
    # ponizej klucz obcy relacyjne pole Post.comments
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Komentarz dodany przez {} dla posta {}'.format(self.name, self.post)






