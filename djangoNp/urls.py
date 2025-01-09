from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from projects.views import (
    ArticleAPIDestroy,
    ArticleAPIList,
    ArticleAPIUpdate,
    CurrentUserView,
    InitiativeAPIDestroy,
    InitiativeAPIList,
    InitiativeAPIUpdate,
    ProjectAPIDestroy,
    ProjectAPIList,
    ProjectAPIUpdate,
    upload_image,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/article/", ArticleAPIList.as_view()),
    path("api/v1/article/<int:pk>/", ArticleAPIUpdate.as_view()),
    path("api/v1/article/<int:pk>/", ArticleAPIDestroy.as_view()),
    path("api/v1/project/", ProjectAPIList.as_view()),
    path("api/v1/project/<int:pk>/", ProjectAPIUpdate.as_view()),
    path("api/v1/project/<int:pk>/", ProjectAPIDestroy.as_view()),
    path("api/v1/initiative/", InitiativeAPIList.as_view()),
    path("api/v1/initiative/<int:pk>/", InitiativeAPIUpdate.as_view()),
    path("api/v1/initiative/<int:pk>/", InitiativeAPIDestroy.as_view()),
    path(
        "api/v1/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"
    ),
    path("api/v1/user/", CurrentUserView.as_view(), name="current_user"),
    path("tinymce/", include("tinymce.urls")),
    path(
        "api/v1/upload/", upload_image, name="upload_image"
    ),  # Подключаем URL вашего приложения
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
