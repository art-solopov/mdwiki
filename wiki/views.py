import markdown
import bleach
from django.http.response import Http404
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView, ModelFormMixin
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse_lazy

from .models import Article
from .forms import ArticleForm


class HomePageView(TemplateView):

    """Home page view"""

    template_name = 'wiki/index.html'
    http_method_names = ['get', 'head']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.order_by('-updated')[:5]
        return context


class ArticleDetailView(View):

    def get(self, request, *args, **kwargs):
        name = kwargs['name']
        self.object = self.get_object(name)
        if self.object is None:
            return redirect('article-edit', name=name)
        self.context = {'article': self.object}
        self.context['compiled_body'] = bleach.clean(
            markdown.markdown(
                self.object.body,
                extensions=[
                    'markdown.extensions.wikilinks'
                ],
                output_format='html5'
            ),
            tags=bleach.ALLOWED_TAGS + ['p']
        )
        return render(request, 'wiki/article_detail.html', context=self.context)

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
            return super().get_object(queryset)
        except Http404:
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
