from django.db import models


class Article(models.Model):
    name = models.CharField('Article name', max_length=1100, db_index=True)
    body = models.TextField('Article body in Markdown')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Alias(models.Model):
    name = models.CharField('Alias', max_length=1100, db_index=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
