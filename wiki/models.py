from django.db import models
from django.core.urlresolvers import reverse_lazy
from markdown import markdown
from .etc import generate_article_link
import re

ARTICLE_NAME_REGEXP = '[\w\s,:?!\-\'"]+'

class Article(models.Model):

    name = models.CharField('Article name', max_length=1100, db_index=True)
    body = models.TextField('Article body in Markdown')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse_lazy('article-detail', kwargs={'name': self.name})

    def __str__(self):
        return self.name

    def body_as_html(self):

        # Preprocessing MD
        mdbody = re.sub(
            '\\[\\[({0})\\]\\]'.format(ARTICLE_NAME_REGEXP),
            lambda match: generate_article_link(match.group(1)),
            self.body
            )

        return markdown(
            mdbody,
            extensions=[
                'markdown.extensions.tables',
                'markdown.extensions.footnotes'
            ],
            output_format='html5'
            )


class Alias(models.Model):
    name = models.CharField('Alias', max_length=1100, db_index=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
