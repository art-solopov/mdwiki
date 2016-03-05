import bleach
from django.views.generic import View, TemplateView, DetailView
from django.views.generic.edit import FormView, ModelFormMixin, CreateView
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
        context['compiled_body'] = bleach.clean(
            self.object.article.body_as_html(),
            tags=self.ALLOWED_TAGS
        )
        return context


class ArticleEditView(FormView, ModelFormMixin):

    form_class = ArticleForm
    model = Article
    template_name = 'wiki/article_edit.html'
    slug_field = 'name'
    slug_url_kwarg = 'name'

    # def get_object(self, queryset=None):
    #     try:
    #         return Article.objects.get(name=self.kwargs['name'])
    #     except Article.DoesNotExist:
    #         return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object() or Article(name=kwargs['name'])
        self.success_url = reverse_lazy(
            'article-detail', kwargs={'name': self.object.name}
        )
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.kwargs['name']
        context['is_new'] = self.object is None
        return context

class NewArticleView(CreateView):

    model = Article
    form_class = NewArticleForm
    template_name = 'wiki/new_article.html'
