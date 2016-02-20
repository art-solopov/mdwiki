import markdown
import bleach
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView, ModelFormMixin, CreateView
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy

from .models import Article
from .forms import ArticleForm, NewArticleForm


class HomePageView(TemplateView):

    """Home page view"""

    template_name = 'wiki/index.html'
    http_method_names = ['get', 'head']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.order_by('-updated')[:5]
        return context


class ArticleDetailView(View):
    ALLOWED_TAGS = (bleach.ALLOWED_TAGS +
                    ['p', 'table', 'tr', 'td', 'th', 'thead', 'tbody'] +
                    [ 'h' + str(i + 1) for i in range(6) ]
    )

    def get(self, request, *args, **kwargs):
        name = kwargs['name']
        self.object = self.get_object(name)
        if self.object is None:
            return render(request, 'wiki/404.html',
                          context={'name': name}, status=404)
        self.context = {'article': self.object}
        self.context['compiled_body'] = bleach.clean(
            self.object.body_as_html(),
            tags=self.ALLOWED_TAGS
        )
        return render(request, 'wiki/article_detail.html',
                      context=self.context)

    def get_object(self, name):
        try:
            return Article.objects.get(name=name)
        except Article.DoesNotExist:
            return None


class ArticleEditView(FormView, ModelFormMixin):

    form_class = ArticleForm
    model = Article
    template_name = 'wiki/article_edit.html'
    slug_field = 'name'
    slug_url_kwarg = 'name'

    def get_object(self, queryset=None):
        try:
            return Article.objects.get(name=self.kwargs['name'])
        except Article.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() or Article(name=kwargs['name'])
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
