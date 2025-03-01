from django.contrib import admin

from .models import Article, ArticleCategory, Initiative, Project


class ExcludeFieldsModelAdmin(admin.ModelAdmin):
    def get_exclude(self, request, obj=None):
        # Получаем все поля модели, заканчивающиеся на '_webp'
        webp_fields = [
            field.name
            for field in self.model._meta.fields
            if field.name.endswith("_webp")
        ]

        # Возвращаем список этих полей для исключения из админки
        return webp_fields

    # Переопределяем метод get_fieldsets для использования динамического exclude
    def get_fieldsets(self, request, obj=None):
        # Получаем список полей, которые нужно исключить
        exclude_fields = self.get_exclude(request, obj)

        # Получаем все существующие fieldsets
        fieldsets = super().get_fieldsets(request, obj)

        # Для каждого fieldset удаляем из него поля, которые нужно исключить
        for fieldset in fieldsets:
            fieldset[1]["fields"] = [
                field
                for field in fieldset[1]["fields"]
                if field not in exclude_fields
            ]

        return fieldsets


admin.site.register(Project, ExcludeFieldsModelAdmin)
admin.site.register(Initiative, ExcludeFieldsModelAdmin)
admin.site.register(Article, ExcludeFieldsModelAdmin)
admin.site.register(ArticleCategory)
