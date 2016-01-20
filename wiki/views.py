from django.shortcuts import render
from django.views.decorators.http import require_safe
from .models import Article


@require_safe
def index(request):
    """Index view for the wiki
    """
    latest = Article.objects.order_by('-updated')[:5]
    return render(request, 'wiki/index.html', {'latest': latest})
