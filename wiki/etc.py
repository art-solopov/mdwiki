from django.core.urlresolvers import reverse_lazy

def generate_article_link(title, url=None):
    if url is None:
        url = reverse_lazy('article-detail', kwargs={'name': title})

    return "[{0}]({1})".format(title, url)
