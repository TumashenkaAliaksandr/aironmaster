from django.contrib import admin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin

from .forms import BannerForm
from .models import ItemPhoto, ItemObject, Banner


class ItemPhotoInline(admin.TabularInline):
    model = ItemPhoto
    fk_name = 'contact_object'
    extra = 1
    max_num = 8
    fields = ('photo', 'description')
    readonly_fields = ()

class ItemObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone1', 'phone2')
    search_fields = ('name', 'description', 'phone1', 'phone2')
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
                ('photo1', 'photo1_description'),
                ('photo2', 'photo2_description'),
                ('photo3', 'photo3_description'),
                ('photo4', 'photo4_description'),
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
