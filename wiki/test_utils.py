import textwrap
import factory
import factory.django as fact_dj
from faker import Faker

from wiki.models import Article, Alias

faker = Faker()

class ArticleFactory(fact_dj.DjangoModelFactory):
    class Meta:
        model = Article

    body = (
        ''.join(faker.paragraphs(nb=2)) +
        textwrap.dedent('''

        Some *test Markdown,* including [[Wiki links]]
        ''')
    )

class AliasFactory(fact_dj.DjangoModelFactory):
    class Meta:
        model = Alias

    name = factory.LazyAttribute(lambda _: faker.company())
    slug = factory.LazyAttribute(lambda _: faker.slug()) # TODO remove when signals are generated
    article = factory.SubFactory(ArticleFactory)


class NewArticleMixin:
    def setUp(self):
        self.article = ArticleFactory.create()
        super().setUp()

class NewAliasMixin:
    def setUp(self):
        super().setUp()
        self.alias = AliasFactory.create()
        self.article = self.alias.article

