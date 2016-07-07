from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from wiki.models import Article, Alias
from wiki.test_utils import NewArticleMixin, NewAliasMixin

class ArticleTestCase(NewArticleMixin, TestCase):

    """Testing the Article model"""

class AliasTestCase(NewAliasMixin, TestCase):

    def test_set_slug(self):
        self.assertEqual(slugify(self.alias.name), self.alias.slug)
