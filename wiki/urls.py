from django.conf.urls import url

from .models import ARTICLE_NAME_REGEXP
from . import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='index'),
    url(
        r'^wiki/(?P<name>{0})$'.format(ARTICLE_NAME_REGEXP),
        views.ArticleDetailView.as_view(), name='article-detail'
    ),
    url(
        r'^wiki/(?P<name>{0})/edit$'.format(ARTICLE_NAME_REGEXP),
        views.ArticleEditView.as_view(), name='article-edit'
    )
]
