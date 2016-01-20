from django.shortcuts import render
from django.views.decorators.http import require_safe
from django.views.generic import TemplateView
from .models import Article


class HomePageView(TemplateView):

    """Home page view"""

    template_name = 'wiki/index.html'
    http_method_names = ['get', 'head']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.order_by('-updated')[:5]
        return context

