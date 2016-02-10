import markdown
import bleach
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import redirect, render

from .models import Article


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

class ArticleEditView(FormView):
    pass


