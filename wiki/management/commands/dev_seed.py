from faker import Factory
from django.core.management.base import BaseCommand
from wiki.models import Article

class Command(BaseCommand):

    """Seed the Article model"""

    def handle(self, *args, **options):
        fake = Factory.create()
        for i in range(10):
            a = Article(
                name=fake.company(),
                body=fake.text(max_nb_chars=500),
            )
            a.save()
