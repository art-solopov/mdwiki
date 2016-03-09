from django.core.urlresolvers import reverse_lazy
from django.utils.text import slugify

def generate_article_link(title, url=None):
    if url is None:
        url = reverse_lazy('article-detail', kwargs={'slug': slugify(title)})

    return "[{0}]({1})".format(title, url)
