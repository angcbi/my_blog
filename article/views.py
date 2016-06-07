from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.utils.encoding import smart_str
from article.models import Article

# Create your views here.
def home(request):
    return HttpResponse("Hello, World")

def detail(request, id):
    try:
        post = Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {'post': post})


def home(request):
    try:
        post_list = Article.objects.all()
    except Exception as e:
        print e
    return render(request, 'home.html', {"post_list": post_list})

def archives(request):
    try:
        post_list = Article.objects.all()
    except Exception,e:
        print e

    return render(request, 'archives.html', {'post_list': 'post_list', 'error': False})
