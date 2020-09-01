from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'email', 'post', 'date', 'published')
    list_editable = ('published',)
    list_display_links = ('id', 'author', 'email')


admin.site.register(Comment, CommentAdmin)
