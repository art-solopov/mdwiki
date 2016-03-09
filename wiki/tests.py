import textwrap

from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Article, Alias

class NewArticleMixin:
    def setUp(self):
        self.article = Article(
            body=textwrap.dedent('''\
            ## This is some test markdown!

            It has [[Wiki links]] and stuff.
            ''')
        )
        self.article.save()
        super().setUp()

class NewAliasMixin(NewArticleMixin):
    def setUp(self):
        super().setUp()
        self.alias = Alias(name='Test alias', slug='test-alias',
                           article=self.article)
        self.alias.save()


class ArticleTestCase(NewArticleMixin, TestCase):

    """Testing the Article model"""

    def test_body_as_html(self):
        self.assertIn(
            reverse('article-detail', kwargs={ 'slug': 'wiki-links' }),
            self.article.body_as_html()
        )


class HomePageViewTestCase(TestCase):

    """Testing the HomePageView"""

    def test_response(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class ArticleDetailViewTestCase(NewAliasMixin, TestCase):

    """ Testing the ArticleDetailView"""

    def test_response(self):
        response = self.client.get(reverse('article-detail',
                                           kwargs={'slug': self.alias.slug}))
        self.assertEqual(response.status_code, 200)

class ArticleEditViewTestCase(NewAliasMixin, TestCase):

    """ Testing the ArticleEditView """

    def test_response(self):
        response = self.client.get(reverse('article-edit',
                                           kwargs={'slug': self.alias.slug}))
        self.assertEqual(response.status_code, 200)
