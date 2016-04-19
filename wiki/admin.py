from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Article, Alias


@admin.register(Article)
class ArticleAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    date_hierarchy = 'modified'
    list_display = ('__str__', 'created', 'modified')

@admin.register(Alias)
class AliasAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created', 'modified')
