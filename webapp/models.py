from django.db import models
from django.core.exceptions import ValidationError

class ItemObject(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    phone1 = models.CharField("Телефон 1", max_length=25)
    phone2 = models.CharField("Телефон 2", max_length=25, blank=True, null=True)

    class Meta:
        verbose_name = "Изделия"
        verbose_name_plural = "Изделия"
        ordering = ['name']

    def __str__(self):
        return self.name



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

