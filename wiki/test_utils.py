import textwrap

from wiki.models import Article, Alias

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

