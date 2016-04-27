from django.test import TestCase

from .models import Article, Alias

class ArticleTestCase(NewArticleMixin, TestCase):

    """Testing the Article model"""

    def test_body_as_html(self):
        self.assertIn(
            reverse('article-detail', kwargs={ 'slug': 'wiki-links' }),
            self.article.body_as_html()
        )
