from django.contrib import admin
from .models import Project, Initiative, Article, ArticleCategory


admin.site.register([Project, Initiative, Article, ArticleCategory])
