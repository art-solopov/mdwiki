import textwrap as tw

from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from model_utils.models import TimeStampedModel
from treebeard.ns_tree import NS_Node

class Article(TimeStampedModel, models.Model):

    body = models.TextField(_('Article body in Markdown'))
    history = HistoricalRecords()
    locale = models.SlugField(max_length=10)

    def name(self):
        return self._main_alias().name

    def slug(self):
        return self._main_alias().slug

    def __str__(self):
        return tw.shorten(self.body, width=70)

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

class Comment(NS_Node):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(_('Comment'))
