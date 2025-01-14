import os

from django.contrib.auth.models import User
from django.db import models
from PIL import Image as PilImage
from tinymce.models import HTMLField

from djangoNp import settings
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def is_absolute_url(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc)


class ImageOptimizationMixin:
    def optimize_image(self, *args, **kwargs):
        if self.image:
            self.compress_image()
            self.create_webp_image()
        else:
            # Если изображение очищено, также очищаем image_webp
            self.image_webp = None

        # super().save(*args, **kwargs)

    def compress_image(self):
        # Открываем оптимизированное оригинальное изображение
        image = PilImage.open(self.image)
        image_name = os.path.basename(self.image.path)
        image_path = os.path.join("media/images/", image_name)

        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        # Конвертируем изображение в RGB, если оно имеет альфа-канал
        if image.mode == "RGBA":
            image = image.convert("RGB")

        # Сохраняем изображение с quality=80 и оптимизацией
        image.save(image_path, format="JPEG", quality=80, optimize=True)

        # Сохраняем путь к новому файлу в поле image_webp
        self.image = image_path.replace("media/", "")  # Обновляем поле image

    def create_webp_image(self):
        # Определяем путь для WebP изображения
        image_name = os.path.basename(self.image.path)
        webp_image_name = os.path.splitext(image_name)[0] + ".webp"
        webp_image_path = os.path.join("media/images/", webp_image_name)
        original_image_path = os.path.join("media/images/", image_name)

        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(webp_image_path), exist_ok=True)

        # Открываем изображение для создания WebP версии
        image = PilImage.open(original_image_path)

        # Сохраняем изображение в формате WebP
        image.save(webp_image_path, format="webp", quality=80)

        # Сохраняем путь к новому файлу в поле image_webp
        self.image_webp = webp_image_path.replace(
            "media/", ""
        )  # Обновляем поле image_webp


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
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    image_webp = models.ImageField(blank=True, null=True)

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
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    initiative_id = models.ForeignKey(Initiative, on_delete=models.CASCADE)
    cat_id = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    image_webp = models.ImageField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # оптимизация изображения, метод из ImageOptimizationMixin
        self.optimize_image(*args, **kwargs)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статья"

    def __str__(self):
        return self.title
