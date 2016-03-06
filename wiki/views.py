import bleach
from django.views.generic import View, TemplateView, DetailView
from django.views.generic.edit import (FormView, ModelFormMixin,
                                       CreateView, UpdateView)
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy

from .models import Article, Alias
from .forms import ArticleForm, NewArticleForm


class HomePageView(TemplateView):

    """Home page view"""

    template_name = 'wiki/index.html'
    http_method_names = ['get', 'head']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = (Article.objects
                                      .prefetch_related('alias_set')
                                      .order_by('-updated')[:5])
        return context


class ArticleDetailView(DetailView):
    ALLOWED_TAGS = (bleach.ALLOWED_TAGS +
                    ['p', 'table', 'tr', 'td', 'th', 'thead', 'tbody'] +
                    [ 'h' + str(i + 1) for i in range(6) ]
    )

    # Yes, model is Alias, because that's what we fetch with the slug
    model = Alias
    template_name = 'wiki/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_name'] = self.object.article.name
        context['compiled_body'] = bleach.clean(
            self.object.article.body_as_html(),
            tags=self.ALLOWED_TAGS
        )
        return context


class ArticleEditView(UpdateView):

    form_class = ArticleForm
    model = Article
    template_name = 'wiki/article_edit.html'
    slug_field = 'alias__slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.object.name()
        return context

    def get_success_url(self):
        return reverse_lazy('article-detail',
                            kwargs={'slug': self.kwargs['slug']})


class NewArticleView(CreateView):

    model = Article
    form_class = NewArticleForm
    template_name = 'wiki/new_article.html'
