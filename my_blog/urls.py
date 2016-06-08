from django.conf.urls import patterns, include, url
from django.contrib import admin
from article.views import RSSFeed

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'article.views.home', name='home'),
    url(r'^archives/$', 'article.views.archives', name='archives'),
    url(r'^(?P<id>\d+)/$', 'article.views.detail', name='detail'),
    url(r'^tag(?P<tag>\w+)/$', 'article.views.search_tag', name='search_tag'),
    url(r'^about_me/$', 'article.views.about_me', name='about_me'),
    url(r'^feed/$', RSSFeed(), name='RSS'),
)
