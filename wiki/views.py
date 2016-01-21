import markdown
import bleach
from django.views.generic import TemplateView, DetailView

from .models import Article


class HomePageView(TemplateView):

    """Home page view"""

    template_name = 'wiki/index.html'
    http_method_names = ['get', 'head']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.order_by('-updated')[:5]
        return context


class ArticleDetailView(DetailView):

    model = Article
    slug_field = 'name'
    slug_url_kwarg = 'name'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['compiled_body'] = bleach.clean(
            markdown.markdown(
                context['article'].body,
                extensions=[
                    'markdown.extensions.wikilinks'
                ]
            )
        )
        return context
