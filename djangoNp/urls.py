from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from projects.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/article/', ArticleAPIList.as_view()),
    path('api/v1/article/<int:pk>/', ArticleAPIUpdate.as_view()),
    path('api/v1/article/<int:pk>/', ArticleAPIDestroy.as_view()),
    path('api/v1/project/', ProjectAPIList.as_view()),
    path('api/v1/project/<int:pk>/', ProjectAPIUpdate.as_view()),
    path('api/v1/project/<int:pk>/', ProjectAPIDestroy.as_view()),
    path('api/v1/initiative/', InitiativeAPIList.as_view()),
    path('api/v1/initiative/<int:pk>/', InitiativeAPIUpdate.as_view()),
    path('api/v1/initiative/<int:pk>/', InitiativeAPIDestroy.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)