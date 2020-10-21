from django.contrib import admin

from .models import BlogCategory, BlogTag, Article, ArticleImage


class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'add_time']


admin.site.register(BlogCategory, BlogCategoryAdmin)


class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'add_time']


admin.site.register(BlogTag, BlogTagAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'user', 'click_num', 'add_time']
    list_filter = ['category', 'user', 'add_time']

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleImage)