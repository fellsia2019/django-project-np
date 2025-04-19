import os
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.db import models
from PIL import Image as PilImage
from tinymce.models import HTMLField

from djangoNp import settings


def is_absolute_url(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc)


class ImageOptimizationMixin:
    def optimize_image(self, *args, **kwargs):
        # Получаем список полей с изображениями (по умолчанию это 'image')
        image_fields = getattr(self, "image_fields", ["image"])

        for field in image_fields:
            image = getattr(self, field, None)
            if image:
                # Оптимизация и создание WebP для каждого изображения
                self.compress_image(field)
                self.create_webp_image(field)
            else:
                # Если изображения нет, очищаем соответствующее поле _webp
                setattr(self, f"{field}_webp", None)

    def compress_image(self, field):
        # Получаем изображение для текущего поля
        image = getattr(self, field)
        image_name = os.path.basename(image.path)
        image_path = os.path.join("media/images/", image_name)

        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        # Открываем изображение с помощью PIL и конвертируем в RGB, если нужно
        pil_image = PilImage.open(image)
        if pil_image.mode == "RGBA":
            pil_image = pil_image.convert("RGB")

        # Сохраняем изображение в JPEG формате с оптимизацией
        pil_image.save(image_path, format="JPEG", quality=80, optimize=True)

        # Обновляем путь в поле изображения
        setattr(self, field, image_path.replace("media/", ""))

    def create_webp_image(self, field):
        # Формируем путь для изображения в формате WebP
        image = getattr(self, field)
        image_name = os.path.basename(image.path)
        webp_image_name = os.path.splitext(image_name)[0] + ".webp"
        webp_image_path = os.path.join("media/images/", webp_image_name)
        original_image_path = os.path.join("media/images/", image_name)

        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(webp_image_path), exist_ok=True)

        # Открываем изображение для конвертации в WebP
        pil_image = PilImage.open(original_image_path)

        # Сохраняем изображение в WebP формате
        pil_image.save(webp_image_path, format="webp", quality=80)

        # Обновляем путь к WebP изображению
        setattr(self, f"{field}_webp", webp_image_path.replace("media/", ""))


class Project(models.Model, ImageOptimizationMixin):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    detail_text = HTMLField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    image_webp = models.ImageField(blank=True, null=True)
    image_detail = models.ImageField(blank=True, null=True)
    image_detail_webp = models.ImageField(blank=True, null=True)
    json_blocks = models.JSONField(blank=True, null=True)

    # Указываем поля с изображениями, которые нужно обрабатывать
    image_fields = ["image", "image_detail"]

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # оптимизация изображения, метод из ImageOptimizationMixin
        self.optimize_image(*args, **kwargs)

        # Заменяем относительные URL на абсолютные перед сохранением
        if self.detail_text:
            self.detail_text = self.convert_relative_to_absolute(
                self.detail_text
            )

        super().save(*args, **kwargs)

    def convert_relative_to_absolute(self, html_content):
        # Базовый URL для формирования абсолютных ссылок
        base_url = f"{settings.SITE_URL}"

        # Используем BeautifulSoup для разбора HTML содержимого
        soup = BeautifulSoup(html_content, "html.parser")

        # Обновляем атрибуты src и data-mce-src
        for img in soup.find_all("img"):
            if img.has_attr("src") and not is_absolute_url(img["src"]):
                relative_src = img["src"]

                img["src"] = f"{base_url}/{relative_src.lstrip('../')}"

        # Возвращаем обновленное содержимое
        return str(soup)


class Initiative(models.Model, ImageOptimizationMixin):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    detail_text = HTMLField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    image_webp = models.ImageField(blank=True, null=True)
    image_detail = models.ImageField(blank=True, null=True)
    image_detail_webp = models.ImageField(blank=True, null=True)
    json_blocks = models.JSONField(blank=True, null=True)

    # Указываем поля с изображениями, которые нужно обрабатывать
    image_fields = ["image", "image_detail"]

    class Meta:
        verbose_name = "Инициатива"
        verbose_name_plural = "Инициатива"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # оптимизация изображения, метод из ImageOptimizationMixin
        self.optimize_image(*args, **kwargs)
        super().save(*args, **kwargs)


class ArticleCategory(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Категория статьи"
        verbose_name_plural = "Категория статьи"

    def __str__(self):
        return self.title


class Article(models.Model, ImageOptimizationMixin):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    detail_text = HTMLField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    initiative_id = models.ForeignKey(Initiative, on_delete=models.CASCADE)
    cat_id = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    image_webp = models.ImageField(blank=True, null=True)
    image_detail = models.ImageField(blank=True, null=True)
    image_detail_webp = models.ImageField(blank=True, null=True)
    json_blocks = models.JSONField(blank=True, null=True)

    # Указываем поля с изображениями, которые нужно обрабатывать
    image_fields = ["image", "image_detail"]

    def save(self, *args, **kwargs):
        # оптимизация изображения, метод из ImageOptimizationMixin
        self.optimize_image(*args, **kwargs)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статья"

    def __str__(self):
        return self.title
