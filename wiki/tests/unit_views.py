from django.test import TestCase
from django.core.urlresolvers import reverse

from utils import NewArticleMixin, NewAliasMixin
from common.tests.utils import UserMixin

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

class ArticleEditViewTestCase(UserMixin, NewAliasMixin, TestCase):

    """ Testing the ArticleEditView """

    def test_form_response(self):
        response = self.client.get(reverse('article-edit',
                                           kwargs={'slug': self.alias.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_form_valid(self):
        response = self.client.post(
            reverse('article-edit', kwargs={'slug': self.alias.slug}),
            {'body': 'New test body'}
        )
        self.article.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.article.body, 'New test body')

    def test_form_invalid(self):
        response = self.client.post(
            reverse('article-edit', kwargs={'slug': self.alias.slug}),
            {'body': ''}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

class NewArticleViewTestCase(UserMixin, TestCase):

    def test_form_response(self):
        response = self.client.get(reverse('new-article'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_form_valid(self):
        response = self.client.post(
            reverse('new-article'),
            {'name': 'Test name', 'slug': 'test-name', 'body': 'Test body'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Alias.objects.count(), 1)
        article = Article.objects.all()[0]
        alias = Alias.objects.all()[0]
        self.assertEqual(article.body, 'Test body')
        self.assertEqual(alias.name, 'Test name')
        self.assertEqual(alias.slug, 'test-name')
        self.assertEqual(alias.article, article)

    def test_form_invalid(self):
        response = self.client.post(
            reverse('new-article'),
            {'name': '', 'slug': '', 'body': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Article.objects.count(), 0)
        self.assertEqual(Alias.objects.count(), 0)
