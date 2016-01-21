from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='index'),
    url(r'^(?P<name>[\w\s]+)', views.ArticleDetailView.as_view(), name='article-detail')
]
