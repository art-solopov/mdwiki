from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='index'),
    url(r'^wiki/(?P<slug>[\w-]+)$', views.ArticleDetailView.as_view(),
        name='article-detail'),
    # url(
    #     r'^wiki/(?P<name>{0})$'.format(ARTICLE_NAME_REGEXP),
    #     views.ArticleDetailView.as_view(), name='article-detail'
    # ),
    # url(
    #     r'^wiki/(?P<name>{0})/edit$'.format(ARTICLE_NAME_REGEXP),
    #     views.ArticleEditView.as_view(), name='article-edit'
    # ),
    url(r'^new_article', views.NewArticleView.as_view(), name='new-article')
]
