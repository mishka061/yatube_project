from django.contrib import admin
from .models import Post, Group, Comment, Follow


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    ordering = ['-pub_date']


#class GroupAdmin(admin.ModelAdmin):
#    list_display = (
#        'pk',
#        'text',
#        'author',
#        'group',
#    )
#    list_editable = ('group',)
#    search_fields = ('text',)
#    empty_value_display = '-пусто-'
#
#
#class CommentAdmin(admin.ModelAdmin):
#    list_display = (
#        'pk',
#        'post'
#        'text',
#        'author',
#        'created'
#    )
#    search_fields = ('text', 'author', 'post')
#    list_filter = ('post',)
#    empty_value_display = '-пусто-'
#
#
#class FollowAdmin(admin.ModelAdmin):
#    list_display = (
#        'pk',
#        'author',
#        'user',
#    )
#    search_fields = ('author', 'user')
#    list_filter = ('author',)
#    empty_value_display = '-пусто-'
#

admin.site.register(Post, PostAdmin)
admin.site.register(Group)
admin.site.register(Comment)
admin.site.register(Follow)
#admin.site.register(Group, GroupAdmin)
#admin.site.register(Comment, CommentAdmin)
#admin.site.register(Follow, FollowAdmin)