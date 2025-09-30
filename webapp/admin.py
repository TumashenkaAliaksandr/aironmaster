from django.contrib import admin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin

from .forms import BannerForm, OurServiceForm, ItemObjectForm, AdvertisementForm, CharaForm
from .models import ItemPhoto, ItemObject, Banner, HadContact, ServicesContact, FooterInfo, About, OurService, \
    SocialNetwork, BannerPage, ServicePhoto, News, ServicePrice, ServiceAdvantage, ServiceVideo, Advertisement, \
    AdvertisementVideo, OurWorks


class ItemPhotoInline(admin.TabularInline):
    model = ItemPhoto
    fk_name = 'contact_object'
    extra = 1
    max_num = 8
    fields = ('photo', 'description')
    readonly_fields = ()

class ItemObjectAdmin(admin.ModelAdmin):
    form = ItemObjectForm
    list_display = ('name', 'mission', 'phone1', 'phone2')
    search_fields = ('name', 'mission', 'description', 'description_more', 'phone1', 'phone2')
    inlines = [ItemPhotoInline]

admin.site.register(ItemObject, ItemObjectAdmin)


@admin.register(Banner)
class BannerAdmin(SummernoteModelAdmin):
    form = BannerForm

    list_display = ('name', 'phone1', 'phone2', 'photo_preview')
    search_fields = ('name', 'phone1', 'phone2')

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'phone1', 'phone2')
        }),
        ('Фотографии', {
            'fields': (
                ('photo1', 'photo1_description', 'photo1_link'),
                ('photo2', 'photo2_description', 'photo2_link'),
                ('photo3', 'photo3_description', 'photo3_link'),
                ('photo4', 'photo4_description', 'photo4_link'),
            ),
        }),
    )

    def photo_preview(self, obj):
        photos = [
            (obj.photo1, obj.photo1_description),
            (obj.photo2, obj.photo2_description),
            (obj.photo3, obj.photo3_description),
            (obj.photo4, obj.photo4_description),
        ]
        imgs = []
        for photo, desc in photos:
            if photo:
                imgs.append(
                    f'<div style="display:inline-block; margin-right:10px; text-align:center;">'
                    f'<img src="{photo.url}" style="max-height: 100px; display:block; margin-bottom:5px;" alt="{desc}"/>'
                    f'<small>{desc}</small>'
                    f'</div>'
                )
        return format_html(''.join(imgs))
    photo_preview.short_description = "Превью фото"


@admin.register(HadContact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')


@admin.register(ServicesContact)
class ServicesContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_one', 'phone_two')
    search_fields = ('name', 'phone_one', 'phone_two')


class SocialNetworkInline(admin.TabularInline):
    model = SocialNetwork
    extra = 1  # количество пустых форм для добавления новых соцсетей
    fields = ('name', 'url', 'icon')
    readonly_fields = ()
    show_change_link = True

@admin.register(FooterInfo)
class FooterInfoAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone_one', 'phone_two', 'email')
    fields = (
        'address',
        ('phone_one', 'phone_two', 'email'),
    )
    inlines = [SocialNetworkInline]


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'photo_preview')
    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 100px; height: auto; border-radius: 4px;" />', obj.photo.url)
        return "Нет фото"
    photo_preview.short_description = "Превью фото"


class ServicePhotoInline(admin.TabularInline):
    model = ServicePhoto
    extra = 1  # сколько пустых форм для добавления новых фото показывать
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto; border-radius: 4px;" />', obj.image.url)
        return "Нет фото"
    image_preview.short_description = "Превью фото"


class ServicePriceInline(admin.TabularInline):
    model = ServicePrice
    extra = 1

class ServiceAdvantageInline(admin.TabularInline):
    model = ServiceAdvantage
    extra = 1


class ServiceVideoInline(admin.TabularInline):
    model = ServiceVideo
    extra = 1
    fields = ('video', 'title')

@admin.register(OurService)
class OurServiceAdmin(admin.ModelAdmin):
    form = OurServiceForm
    list_display = ('name', 'photo_preview')
    search_fields = ('name', 'description')
    readonly_fields = ('photo_preview',)
    inlines = [ServicePhotoInline, ServiceVideoInline, ServicePriceInline, ServiceAdvantageInline]

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 100px; height: auto; border-radius: 4px;" />',
                obj.photo.url
            )
        return "Нет фото"
    photo_preview.short_description = "Превью фото"


# @admin.register(FinishedProduct)
# class FinishedProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'photo_preview')
#     search_fields = ('name', 'description')
#     readonly_fields = ('photo_preview',)
#
#     def photo_preview(self, obj):
#         if obj.photo:
#             return format_html(
#                 '<img src="{}" style="width: 100px; height: auto; border-radius: 4px;" />',
#                 obj.photo.url
#             )
#         return "Нет фото"
#     photo_preview.short_description = "Превью фото"


@admin.register(BannerPage)
class BannerPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'image_preview')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Превью изображения"


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'date', 'is_main')
    prepopulated_fields = {'slug': ('name',)}  # Автоматическое заполнение слага в админке
    search_fields = ('name', 'description', 'news_text')
    list_filter = ('is_main', 'date')
    ordering = ('-date',)


class AdvertisementVideoInline(admin.TabularInline):
    model = AdvertisementVideo
    extra = 1  # количество пустых форм для добавления видео


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    form = AdvertisementForm  # если вы используете кастомную форму, иначе уберите эту строку
    list_display = ('title',)
    search_fields = ('title', 'description', 'advantages')
    list_per_page = 20

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image')  # удалено 'video'
        }),
        ('Дополнительные данные', {
            'fields': ('advantages', 'additional_description'),
            'classes': ('collapse',),
        }),
    )

    inlines = [AdvertisementVideoInline]  # подключаем inline с видео

@admin.register(AdvertisementVideo)
class AdvertisementVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'advertisement')
    search_fields = ('title', 'advertisement__title')

@admin.register(OurWorks)
class OurWorksAdmin(admin.ModelAdmin):
    form = CharaForm
    list_display = ('title', 'characteristics', 'description', 'photo')
    search_fields = ('title', 'description')


