from django.urls import path
from django.conf.urls import url
from . import views
from .feeds import LatestPostFeed
app_name='blog_2'
urlpatterns = [
    path('', views.Post_list, name='Post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', views.Post_list, name='post_list_by_tag'),
    path('feed/',LatestPostFeed(), name='post_feed'),
    path('new_post/', views.new_post, name='new_post'),



]