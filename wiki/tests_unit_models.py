from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from .models import Article, Alias
from .test_utils import NewArticleMixin, NewAliasMixin

class ArticleTestCase(NewArticleMixin, TestCase):

    """Testing the Article model"""

    def test_body_as_html(self):
        self.assertIn(
            reverse('article-detail', kwargs={ 'slug': 'wiki-links' }),
            self.article.body_as_html()
        )

class AliasTestCase(NewAliasMixin, TestCase):

    def test_set_slug(self):
        self.assertEqual(slugify(self.alias.name), self.alias.slug)
