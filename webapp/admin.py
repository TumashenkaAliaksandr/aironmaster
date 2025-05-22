from django.contrib import admin
from .models import ItemPhoto, ItemObject


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
