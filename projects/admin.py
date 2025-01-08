from django.contrib import admin

from .models import Article, ArticleCategory, Initiative, Project


class ExcludeFieldsModelAdmin(admin.ModelAdmin):
    exclude = ("image_webp",)  # Исключаем поле image_webp из админки


admin.site.register(Project, ExcludeFieldsModelAdmin)
admin.site.register(Initiative, ExcludeFieldsModelAdmin)
admin.site.register(Article, ExcludeFieldsModelAdmin)
admin.site.register(ArticleCategory)
