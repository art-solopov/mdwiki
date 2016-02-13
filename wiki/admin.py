from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ('__str__', 'created', 'updated')
