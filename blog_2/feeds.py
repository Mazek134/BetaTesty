# kanal RSS

from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

class LatestPostFeed(Feed):
    title = 'moj blog'
    link = '/blog_2'
    description = 'Nowe posty na moim blogu'

    def items(self):
        return Post.published.all()[:5]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return  truncatewords(item.body, 30)
