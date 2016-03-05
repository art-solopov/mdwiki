import re

from django.db import models
from markdown import markdown

from .etc import generate_article_link

class Article(models.Model):

    body = models.TextField('Article body in Markdown')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def name(self):
        return self._main_alias().name

    def slug(self):
        return self._main_alias().slug

    def body_as_html(self):
        '''Converting the model's body into HTML
        TODO: Move to helper?
        '''

        # Preprocessing MD
        mdbody = re.sub(
            '\\[\\[(.*?)\\]\\]',
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

    def _main_alias(self):
        return self.alias_set.all()[0]


class Alias(models.Model):
    name = models.CharField('Alias', max_length=1100, db_index=True)
    slug = models.SlugField('Slug', max_length=1100)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
