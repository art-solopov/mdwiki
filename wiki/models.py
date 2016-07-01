import re
import textwrap as tw

from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords
from model_utils.models import TimeStampedModel
from markdown import markdown

from wiki.etc import generate_article_link

class Article(TimeStampedModel, models.Model):

    body = models.TextField(_('Article body in Markdown'))
    history = HistoricalRecords()
    locale = models.SlugField(max_length=10, editable=False)

    def name(self):
        return self._main_alias().name

    def slug(self):
        return self._main_alias().slug

    def __str__(self):
        return tw.shorten(self.body, width=70)

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
        return self.alias_set.order_by('created')[0]


class Alias(TimeStampedModel, models.Model):
    name = models.CharField(_('Alias'), max_length=1100, db_index=True, unique=True)
    slug = models.SlugField(_('Slug'), max_length=1100, db_index=True, unique=True,
                            editable=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} [{1}]".format(self.name, self.slug)

@receiver(pre_save, sender=Alias)
def set_slug(instance, *args, **kwargs):
    instance.slug = slugify(instance.name, allow_unicode=True)
