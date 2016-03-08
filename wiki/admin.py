from django.contrib import admin
from .models import Article, Alias


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ('__str__', 'created', 'updated')

@admin.register(Alias)
class AliasAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created', 'article')
