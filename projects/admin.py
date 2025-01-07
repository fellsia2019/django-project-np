from django.contrib import admin
from .models import Project, Initiative, Article, ArticleCategory


class ProjectAdmin(admin.ModelAdmin):
    exclude = ('image_webp',)  # Исключаем поле image_webp из админки


admin.site.register(Project, ProjectAdmin)
admin.site.register(Initiative)
admin.site.register(Article)
admin.site.register(ArticleCategory)
