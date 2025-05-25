from django.db import models
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class ItemObject(models.Model):
    name = models.CharField("Название", max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    description = models.TextField("Описание")
    phone1 = models.CharField("Телефон 1", max_length=25)
    phone2 = models.CharField("Телефон 2", max_length=25, blank=True, null=True)

    class Meta:
        verbose_name = "Изделия"
        verbose_name_plural = "Изделия"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Если slug пустой, генерируем уникальный slug
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Проверяем уникальность slug в базе
            while ItemObject.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)




class ItemPhoto(models.Model):
    contact_object = models.ForeignKey(
        ItemObject,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name="Объект изделия"
    )
    photo = models.ImageField("Фото", upload_to='contact_photos/')
    description = models.CharField("Описание фото", max_length=255, blank=True)

    class Meta:
        verbose_name = "Фото изделия"
        verbose_name_plural = "Фото изделия"

    def __str__(self):
        return f"Фото для {self.contact_object.name} ({self.description[:20]})"

    def clean(self):
        # Проверяем, что contact_object сохранён и имеет pk
        if self.contact_object and self.contact_object.pk:
            # Ограничение на максимум 8 фото на объект
            if self.contact_object.photos.exclude(pk=self.pk).count() >= 8:
                raise ValidationError("Максимум 8 фотографий на один объект.")



class Banner(models.Model):
    name = models.CharField("Имя", max_length=255)
    description = models.TextField("Описание", blank=True)
    phone1 = models.CharField("Телефон 1", max_length=20, blank=True)
    phone2 = models.CharField("Телефон 2", max_length=20, blank=True)

    photo1 = models.ImageField("Фото 1", upload_to='banners/', blank=True, null=True)
    photo1_description = models.CharField("Описание фото 1", max_length=255, blank=True)

    photo2 = models.ImageField("Фото 2", upload_to='banners/', blank=True, null=True)
    photo2_description = models.CharField("Описание фото 2", max_length=255, blank=True)

    photo3 = models.ImageField("Фото 3", upload_to='banners/', blank=True, null=True)
    photo3_description = models.CharField("Описание фото 3", max_length=255, blank=True)

    photo4 = models.ImageField("Фото 4", upload_to='banners/', blank=True, null=True)
    photo4_description = models.CharField("Описание фото 4", max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"

