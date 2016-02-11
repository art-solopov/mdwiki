from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='index'),
    url(r'^wiki/(?P<name>[\w\s,:?!\-\'"]+)$', views.ArticleDetailView.as_view(), name='article-detail'),
    url(r'^wiki/(?P<name>[\w\s,:?!\-\'"]+)/edit$', views.ArticleEditView.as_view(), name='article-edit')
]
