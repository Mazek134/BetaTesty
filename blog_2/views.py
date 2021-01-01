from django.shortcuts import render
from taggit.models import Tag
# Create your views here.
from django.db.models import Count
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment
from .forms import CommentForm, new_postForm, search_form


def home(request):
    return render(request, 'blog_2/base.html')

def Post_list(request,tag_slug=None): #domyslnie nie ma taga

        object_list = Post.published.all()
        tag = None
        keyword2="poczatkowe"
        result=None
        searched = False
        if request.method == 'POST':
            s_form = search_form(data=request.POST)

            if s_form.is_valid():
                searched = True
                keyword2 = s_form.cleaned_data['keyword']

                object_list= Post.published.filter(title__icontains=keyword2)

                if not  object_list:
                    object_list = Post.published.filter(body__icontains=keyword2)
                if  object_list:
                    result = True

        else:
            s_form = search_form()

        if tag_slug:

            tag = get_object_or_404(Tag,slug=tag_slug)
            object_list = object_list.filter(tags__in=[tag])



        paginator = Paginator(object_list, 3)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts= paginator.page(paginator.num_pages)

        return render(request, 'blog_2/post_list.html', {'page': page, 'posts': posts, 'tag':tag,'s_form':s_form,'result':result, 'searched':searched })

def post_detail(request, year,month, day,post):
    post = get_object_or_404(Post, slug=post,status='published',publish__year = year,publish__month = month,publish__day = day)


    comments = post.comments.filter(active=True) # dzieki related name mozna uzyc post.comments

    if request.method == 'POST':
        # Komentarz został opublikowany.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Utworzenie obiektu Comment, ale jeszcze nie zapisujemy go w bazie danych.
            new_comment = comment_form.save(commit=False)
            new_comment.name = request.user

            # Przypisanie komentarza do bieżącego posta.
            new_comment.post = post
            # Zapisanie komentarza w bazie danych.
            new_comment.save()
    else:
        comment_form = CommentForm()
        #agregate do obliczen np avg srednia
        # annotate do ulozenia wynikow np po liczbie wspolnych tagow
    post_tags_ids = post.tags.values_list('id',flat=True) # zracane sa krotki z wattosciami z danych pol
    similar_posts = Post.published.filter(tags__in = post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags= Count('tags')).order_by('same_tags','-publish')[:3]
    return render(request, 'blog_2/post_detail.html', {'post': post,'comments':comments,'comment_form':comment_form,'similar_posts':similar_posts})

@login_required()
def new_post(request):

    if request.method == 'POST':

        new_post = new_postForm(data=request.POST)

        if new_post.is_valid():

            #wazne dopisanie czegos z autoamtu do form
            post = new_post.save(commit=False)

            post.author = request.user
            post.slug = post.title[:3]
            post.save()
            # zapis many to many aby tagi sie zpisaly z form
            new_post.save_m2m()
            messages.success(request, 'Pomyslnie dodano nowy Post')
        else:
            messages.warning(request,'uzupelnij poprawnie wszystkie pola')
    new_post = new_postForm()
    return render(request, 'blog_2/new_post.html',{'new_post':new_post,})

