from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from article.models import Article

# Create your views here.
def detail(request, id):
    try:
        post = Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {'post': post})


def home(request):
    posts = Article.objects.all()
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.paginator(paginator.num_pages)

    return render(request, 'home.html', {"post_list": post_list})

def archives(request):
    try:
        post_list = Article.objects.all()
    except Exception,e:
        print e

    return render(request, 'archives.html', {'post_list': post_list, 'error': False})

def about_me(request):
    return render(request, 'about_me.html')

def search_tag(request, tag):
    try:
        post_list = Article.objects.filter(category__icontains=tag)
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'tag.html', {'post_list': post_list})

class RSSFeed(Feed):
    title = "RSS feed - article"
    link = "feeds/posts/"
    description = 'Rss fedd - blog posts'

    def items(self):
        return Article.objects.order_by('-date_time')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date_time

    def item_description(self, item):
        return item.content


