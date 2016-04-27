from django.contrib.auth.models import User
from django.test import RequestFactory

class UserMixin:
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username='testuser',
                                             password='test')
        self.client.login(username='testuser', password='test')

class RequestFactoryMixin:
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
