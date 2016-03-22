from django.conf.urls import include, url
from django.contrib import admin

from generic_tagging_example.blog.views import ArticleListView, ArticleDetailView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<pk>\d+)/$',
        ArticleDetailView.as_view(), name='blog_article_detail'),
    url(r'^$', ArticleListView.as_view(), name='blog_article_list'),
]
