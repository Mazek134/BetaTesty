from django import template
from django.db.models import Count
register = template.Library()
from ..models import Post
# tag ktory jest zmienna liczba postow
@register.simple_tag()
def total_posts():
    return Post.published.count()
#tag generuje szablon ktory mozna uzyc wszedzie
@register.inclusion_tag('blog_2/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}
# tag ktory przechowuje wynik w zmiennej (posty najczesciej komentowane)
@register.simple_tag()
def get_most_commented_posts(count=3):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
@register.simple_tag()
def search(keyword):
    return Post.published.filter(title__icontaines=keyword)

