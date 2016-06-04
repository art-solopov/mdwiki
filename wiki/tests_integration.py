import os
from selenium import webdriver
from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from wiki.test_utils import seed_article_data
from wiki.models import Article

DRIVERS = {
    'firefox': webdriver.Firefox,
    'phantomjs': webdriver.PhantomJS
}

DEFAULT_DRIVER = 'firefox'

class WikiIntegrationTest(LiveServerTestCase):

    def setUp(self):
        seed_article_data()
        driver_name = os.environ.get('INTEGRATION_TEST_DRIVER', DEFAULT_DRIVER)
        self.browser = DRIVERS[driver_name]
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(2)

    def test_article_show_page(self):
        self.article = Article.objects.first()
        page = self.browser.get(
            self.live_server_url +
            reverse('article-detail', kwargs={'slug': self.article.slug()})
        )
        title = self.browser.find_element_by_css_selector('h1')
        self.assertEqual(self.article.name(), title.text)
        # self.fail('Incomplete test')
