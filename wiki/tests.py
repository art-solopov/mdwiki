import textwrap

from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Article

class ArticleTestCase(TestCase):

    """Testing the Article model"""

    def setUp(self):
        Article.objects.create(
            name='Test article',
            body=textwrap.dedent('''\
            ## This is some test markdown!

            It has [[Wiki links]] and stuff.
            ''')
        )

    def test_body_as_html(self):
        article = Article.objects.get(name='Test article')
        self.assertIn(
            reverse('article-detail', kwargs={ 'name': 'Wiki links' }),
            article.body_as_html()
        )


class HomePageViewTestCase(TestCase):

    """Testing the HomePageView"""

    def test_response(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
