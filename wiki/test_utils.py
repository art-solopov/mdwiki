from random import random as rnd
import textwrap
import factory
import factory.django as fact_dj
from faker import Faker

from wiki.models import Article, Alias

faker = Faker()

def generate_body():
    lorem = "\n\n".join(faker.paragraphs(nb=2))
    test_markdown = textwrap.dedent('''
        Some *test Markdown,* including [[Wiki links]]
        ''')
    return lorem + "\n\n" + test_markdown

class ArticleFactory(fact_dj.DjangoModelFactory):
    class Meta:
        model = Article

    body = factory.LazyFunction(generate_body)
    locale = 'en'


class AliasFactory(fact_dj.DjangoModelFactory):
    class Meta:
        model = Alias

    name = factory.Faker('company')

    article = factory.SubFactory(ArticleFactory)

def seed_article_data():
    for _ in range(10):
        alias = AliasFactory.create()
        if rnd() < 0.2:
            AliasFactory.create(article=alias.article)

class NewArticleMixin:
    def setUp(self):
        self.article = ArticleFactory.create()
        super().setUp()

class NewAliasMixin:
    def setUp(self):
        super().setUp()
        self.alias = AliasFactory.create()
        self.article = self.alias.article
