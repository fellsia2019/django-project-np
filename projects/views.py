from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Article, Initiative, Project
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (
    ArticleSerializer,
    InitiativeSerializer,
    ProjectSerializer,
    UserSerializer,
)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from PIL import Image
import io


class CustomPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        # Вычисляем общее количество страниц
        total_pages = self.page.paginator.num_pages

        # Текущее положение (offset) в зависимости от текущей страницы и размера страницы
        current_page = self.page.number  # Текущая страница
        page_size = self.get_page_size(self.request)  # Текущий лимит
        offset = (
            (current_page - 1) * page_size if current_page > 0 else 0
        )  # Смещение

        return Response(
            {
                "pagination": {
                    "count": self.page.paginator.count,
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "limit": page_size,
                    "offset": offset,
                    "total_pages": total_pages,
                    "current_page": current_page,
                },
                "results": data,
            }
        )


def create_views(model_class, serializer_model_class):

    class ListCreateView(generics.ListCreateAPIView):
        queryset = model_class.objects.filter(is_published=True).order_by("id")
        serializer_class = serializer_model_class
        permission_classes = (IsAuthenticatedOrReadOnly,)
        pagination_class = CustomPagination

    class UpdateView(generics.RetrieveUpdateAPIView):
        queryset = model_class.objects.all()
        serializer_class = serializer_model_class
        permission_classes = (IsOwnerOrReadOnly,)

    class DestroyView(generics.RetrieveDestroyAPIView):
        queryset = model_class.objects.all()
        serializer_class = serializer_model_class
        permission_classes = (IsAdminOrReadOnly,)

    return ListCreateView, UpdateView, DestroyView


ProjectAPIList, ProjectAPIUpdate, ProjectAPIDestroy = create_views(
    Project, ProjectSerializer
)
InitiativeAPIList, InitiativeAPIUpdate, InitiativeAPIDestroy = create_views(
    Initiative, InitiativeSerializer
)
ArticleAPIList, ArticleAPIUpdate, ArticleAPIDestroy = create_views(
    Article, ArticleSerializer
)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


# @csrf_exempt
# def upload_image(request):
#     if request.method == "POST" and request.FILES.get("file"):
#         file = request.FILES["file"]
#
#         # Сохранение изображения
#         fs = FileSystemStorage()
#         filename = fs.save(file.name, file)  # Сохранение файла в MEDIA_ROOT
#         file_url = fs.url(filename)  # Получение URL к файлу
#
#         return JsonResponse({"location": file_url})
#
#     return JsonResponse({"error": "Upload failed"}, status=400)
@csrf_exempt
def upload_image(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]

        # Сохранение изображения
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)  # Сохранение файла в MEDIA_ROOT
        file_url = fs.url(filename)  # Получение URL к файлу

        # Создание абсолютного URL
        absolute_url = request.build_absolute_uri(file_url)

        # return JsonResponse({"location": file_url})
        return JsonResponse({"location": absolute_url})

    return JsonResponse({"error": "Upload failed"}, status=400)
