import bleach
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import (FormView, CreateView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db import transaction

from .models import Article, Alias
from .forms import ArticleForm, NewArticleForm, AliasForm


class HomePageView(TemplateView):

    """Home page view"""

    template_name = 'wiki/index.html'
    http_method_names = ['get', 'head']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = (Article.objects
                                      .prefetch_related('alias_set')
                                      .order_by('-modified')[:5])
        return context


class ArticleDetailView(DetailView):
    ALLOWED_TAGS = (bleach.ALLOWED_TAGS +
                    ['p', 'table', 'tr', 'td', 'th', 'thead', 'tbody'] +
                    ['h' + str(i + 1) for i in range(6)])

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


class ArticleEditView(LoginRequiredMixin, UpdateView):

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


class NewArticleView(LoginRequiredMixin, FormView):

    form_class = NewArticleForm
    template_name = 'wiki/new_article.html'

    def form_valid(self, form):
        with transaction.atomic():
            self.article = Article(body=form.cleaned_data['body'])
            self.article.save()
            self.main_alias = Alias(
                name=form.cleaned_data['name'],
                article=self.article
            )
            self.main_alias.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article-detail',
                            kwargs={'slug': self.main_alias.slug})

class NewAliasView(LoginRequiredMixin, CreateView):

    form_class = AliasForm
    template_name = 'wiki/new_alias.html'

    def form_valid(self, form):
        article = Article.objects.get(alias__slug=self.kwargs['slug'])
        form.instance.article = article
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article-detail',
                            kwargs={'slug': self.object.slug})
