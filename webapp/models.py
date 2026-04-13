from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify



class OurService(models.Model):
    name = models.CharField("Название сервиса", max_length=255)
    description = models.TextField("Описание", blank=True)
    technology = models.TextField("Технология", blank=True)
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

class ServiceVideo(models.Model):
    service = models.ForeignKey(OurService, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField("Видео", upload_to='service_videos/')
    title = models.CharField("Название видео", max_length=255, blank=True)


class ServiceAdvantage(models.Model):
    service = models.ForeignKey(OurService, related_name='advantages', on_delete=models.CASCADE)
    icon = models.FileField("Иконка преимущества", upload_to='service_advantages_icons/')
    text = models.CharField("Текст преимущества", max_length=255)

    class Meta:
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"

    def __str__(self):
        return self.text


class ItemObject(models.Model):
    name = models.CharField("Название", max_length=255)
    mission = models.CharField("Предназначение", max_length=255, blank=True, null=True)
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
    is_main_top = models.BooleanField("На главную (в верх)", default=False)
    is_stok = models.BooleanField("На складе", default=False)
    is_promotions = models.BooleanField("В акцию", default=False)

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
    photo1_link = models.URLField("Ссылка для фото 1", blank=True)

    photo2 = models.ImageField("Фото 2", upload_to='banners/', blank=True, null=True)
    photo2_description = models.CharField("Описание фото 2", max_length=255, blank=True)
    photo2_link = models.URLField("Ссылка для фото 2", blank=True)

    photo3 = models.ImageField("Фото 3", upload_to='banners/', blank=True, null=True)
    photo3_description = models.CharField("Описание фото 3", max_length=255, blank=True)
    photo3_link = models.URLField("Ссылка для фото 3", blank=True)

    photo4 = models.ImageField("Фото 4", upload_to='banners/', blank=True, null=True)
    photo4_description = models.CharField("Описание фото 4", max_length=255, blank=True)
    photo4_link = models.URLField("Ссылка для фото 4", blank=True)

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


class News(models.Model):
    name = models.CharField('Название', max_length=255, unique=True)
    slug = models.SlugField('Слаг', max_length=255, unique=True, blank=True)
    description = models.TextField('Краткое описание')
    news_text = models.TextField('Основной текст новости')  # Новое поле "текст новости"
    date = models.DateField('Дата публикации')
    photo = models.ImageField('Фото новости', upload_to='news_photos/')
    is_main = models.BooleanField('Главная новость', default=False)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-date']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Автоматическая генерация слага из имени, если не задан
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # URL с использованием slug вместо pk
        return reverse('news_detail', kwargs={'slug': self.slug})


class Advertisement(models.Model):
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание")
    image = models.ImageField("Фото", upload_to='ads/')
    advantages = models.TextField("Преимущества", blank=True, help_text="Опишите основные преимущества")
    additional_description = models.TextField("Дополнительное описание", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Реклама"
        verbose_name_plural = "Реклама"

class AdvertisementVideo(models.Model):
    advertisement = models.ForeignKey(Advertisement, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField("Название видео", max_length=200, blank=True)
    video = models.FileField("Видео", upload_to='service_videos/')

    def __str__(self):
        return self.title or f"Видео для {self.advertisement.title}"

class OurWorks(models.Model):
    title = models.CharField("Имя", max_length=200, blank=True)
    description = models.TextField("Описание")
    characteristics = models.TextField("Характеристики", null=True, blank=True, default=" ")
    photo = models.ImageField("Фото", upload_to='our_works/', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Наши работы"
        verbose_name_plural = "Наша работа"


class ProcessedMetal(models.Model):
    name = models.CharField(max_length=100, verbose_name="Hазвание металла")
    photo = models.ImageField(upload_to='metal_photos/', verbose_name="Фото металла", blank=True, null=True)

    class Meta:
        verbose_name = "Обрабатываемый металл"
        verbose_name_plural = "Обрабатываемые металлы"

    def __str__(self):
        return self.name


class ServicePrice(models.Model):
    service = models.ForeignKey(OurService, related_name='prices', on_delete=models.CASCADE)
    metal_type = models.ForeignKey(
        ProcessedMetal,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Тип металла",
        related_name='serviceprice_metal_type'
    )
    # metal_type_new = models.ForeignKey(
    #     ProcessedMetal,
    #     null=True,
    #     blank=True,
    #     on_delete=models.CASCADE,
    #     verbose_name="Новый тип металла (ForeignKey)",
    #     related_name='serviceprice_metal_type_new'
    # )
    thickness = models.DecimalField("Толщина металла, мм", max_digits=5, decimal_places=2)
    cost = models.DecimalField("Стоимость BYN (без НДС)", max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Стоимость услуги"
        verbose_name_plural = "Стоимость услуг"
        ordering = ['metal_type', 'thickness']

    def __str__(self):
        return f"{self.metal_type.name} - {self.thickness} мм - {self.cost} BYN"


class MetalworkingService(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='services/')
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Блок металлообработка"
        verbose_name_plural = "Блок металлообработка"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})


class SiteBarCategory(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    title = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='category_icons/')
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Сайт Бар Категории"
        verbose_name_plural = "Сайт Бар Категории"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products_by_category', kwargs={'category': self.slug})


class ThreeDConstructions(models.Model):
    name = models.CharField('Имя', max_length=100, blank=True)
    descriptions = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = "3D Моделирование (описание)"
        verbose_name_plural = "3D Моделирование (описание)"

    def __str__(self):
        return self.name


class AdventureService(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='services_for/')
    alt_text = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=50, choices=BannerPage.CATEGORY_CHOICES, blank=True)

    class Meta:
        verbose_name = "Блок Для"
        verbose_name_plural = "Блок Для"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Формируем url для фильтрации продуктов по категории
        return reverse('products_by_category', kwargs={'slug': self.category})
