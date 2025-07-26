from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify



class OurService(models.Model):
    name = models.CharField("Название сервиса", max_length=255)
    description = models.TextField("Описание", blank=True)
    photo = models.ImageField("Фото", upload_to='service_photos/', blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "🛠️ Наш сервис"
        verbose_name_plural = "🛠️ Наши сервисы"
        ordering = ['name']

    def __str__(self):
        return self.name

class ServicePhoto(models.Model):
    service = models.ForeignKey(OurService, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField("Фото", upload_to='service_photos/')




class ItemObject(models.Model):
    name = models.CharField("Название", max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    description = models.TextField("Описание")
    description_more = models.TextField("Описание", null=True, blank=True)
    phone1 = models.CharField("Телефон 1", max_length=25)
    phone2 = models.CharField("Телефон 2", max_length=25, blank=True, null=True)

    # Связь с сервисом (каждое изделие относится к одному сервису)
    service = models.ForeignKey(
        OurService,
        on_delete=models.SET_NULL,  # при удалении сервиса поле станет NULL
        null=True,
        blank=True,
        related_name='items',
        verbose_name="Сервис"
    )

    # Новые булевые поля (галочки)
    is_metal_structures = models.BooleanField("Металлоконструкции", default=False)
    is_prokladki_mtgr = models.BooleanField("Прокладки", default=False)
    is_steps_and_stairs = models.BooleanField("Ступеньки и Лестницы", default=False)
    is_grills = models.BooleanField("Мангалы", default=False)
    is_decor_elements = models.BooleanField("Элементы декора", default=False)
    is_main = models.BooleanField("На главную", default=False)

    class Meta:
        verbose_name = "🎷 Изделия"
        verbose_name_plural = "🎷 Изделия"
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
        verbose_name = "🖼️ Фото изделия"
        verbose_name_plural = "🖼️ Фото изделия"

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
        verbose_name = "🌄 Баннер"
        verbose_name_plural = "🌄 Баннеры"


class HadContact(models.Model):
    name = models.CharField("Имя", max_length=100)
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Почта", max_length=254)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Шапка - 📞 Телефон и 📧 Почта"
        verbose_name_plural = "Шапка - 📞 Телефон и 📧 Почта"


class ServicesContact(models.Model):
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание", blank=True)
    phone_one = models.CharField("Телефон1", max_length=20)
    phone_two = models.CharField("Телефон2", max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуги 👷🏻‍♂️ в Болке Формы - 📞 Телефоны"
        verbose_name_plural = "Услуги 👷🏻‍♂️ в Болке Формы - 📞 Телефоны"


class FooterInfo(models.Model):
    address = models.CharField("Адрес", max_length=255)
    phone_one = models.CharField("Телефон 1", max_length=20)
    phone_two = models.CharField("Телефон 2", max_length=20, blank=True)
    email = models.EmailField("Почта", max_length=254, default='aironmaster@tut.by')

    def __str__(self):
        return "Информация для футера"

    class Meta:
        verbose_name = "🚧 Информация футера"
        verbose_name_plural = "🚧 Информация футера"


class SocialNetwork(models.Model):
    footer_info = models.ForeignKey(
        FooterInfo,
        on_delete=models.CASCADE,
        related_name='social_networks',
        verbose_name="Футер"
    )
    name = models.CharField("Название соцсети", max_length=50)
    url = models.URLField("Ссылка", blank=True)
    icon = models.ImageField("Иконка", upload_to='social_icons/', blank=True, null=True)

    class Meta:
        verbose_name = "Социальная сеть"
        verbose_name_plural = "Социальные сети"

    def __str__(self):
        return self.name



class About(models.Model):
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание", blank=True)
    photo = models.ImageField("Фото", upload_to='about_photos/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ℹ️ О компании"
        verbose_name_plural = "ℹ️ О компании"


# class FinishedProduct(models.Model):
#     name = models.CharField("Название", max_length=255)
#     description = models.TextField("Описание", blank=True)
#     photo = models.ImageField("Фото", upload_to='finished_products/', blank=True, null=True)
#
#     class Meta:
#         verbose_name = "✅ Готовая продукция"
#         verbose_name_plural = "✅ Готовая продукция"
#         ordering = ['name']
#
#     def __str__(self):
#         return self.name


class BannerPage(models.Model):
    CATEGORY_CHOICES = [
        ('metal_structures', 'Металлоконструкции'),
        ('procladki', 'Прокладки'),
        ('steps_and_stairs', 'Ступеньки и Лестницы'),
        ('grills', 'Мангалы'),
        ('decor_elements', 'Элементы декора'),
    ]

    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Фото", upload_to='banners/')
    category = models.CharField("Категория", max_length=50, choices=CATEGORY_CHOICES, unique=True)

    class Meta:
        verbose_name = "⛵ Баннер страницы"
        verbose_name_plural = "⛵ Баннеры страниц"
        ordering = ['name']

    def __str__(self):
        return f"{self.get_category_display()} - {self.name}"
