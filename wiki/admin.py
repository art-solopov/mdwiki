from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from wiki.models import Article, Alias, Comment

@admin.register(Article)
class ArticleAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    date_hierarchy = 'modified'
    list_display = ('__str__', 'created', 'modified')

@admin.register(Alias)
class AliasAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created', 'modified')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('id', 'article', 'user', '__str__', 'removed')
    list_display_links = ('id', '__str__')
    list_filter = ('article', 'user')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('user', 'article')

    actions = ['remove_comment']

    def remove_comment(self, request, queryset):
        queryset.update(
            comment="Removed by {0}".format(request.user.username),
            removed=True
        )

    remove_comment.short_description = 'Remove the comment'
