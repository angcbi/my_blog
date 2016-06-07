from django.shortcuts import render
from django.http import HttpResponse
from django.utils.encoding import smart_str
from article.models import Article

# Create your views here.
def home(request):
    return HttpResponse("Hello, World")

def detail(request, my_args):
    post = Article.objects.all()[int(my_args)]
    str = u'title = {}, category = {}, date_time = {}, content = {}'.format(post.title, post.category, post.date_time, post.content)
    return HttpResponse(str)

def home(request):
    try:
        post_list = Article.objects.all()
    except Exception as e:
        print e
    return render(request, 'home.html', {"post_list": post_list})
