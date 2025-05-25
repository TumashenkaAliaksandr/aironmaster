from django.shortcuts import render, get_object_or_404

from webapp.models import ItemObject, Banner


def index(request):
    item = get_object_or_404(ItemObject, pk=1)
    items = ItemObject.objects.prefetch_related('photos').distinct()

    # Получаем баннер с id=1
    banner = get_object_or_404(Banner, pk=1)

    # Формируем список фото с описаниями из баннера
    photose = []
    for i in range(1, 5):
        photo = getattr(banner, f'photo{i}')
        description = getattr(banner, f'photo{i}_description')
        if photo:
            photose.append({'photo': photo, 'description': description})

    # Получаем фотографии для item (ItemObject)
    photos = item.photos.all()

    context = {
        'item': item,
        'items': items,
        'photos': photos,
        'banner': [banner],   # чтобы можно было итерировать в шаблоне
        'photose': photose,
    }
    return render(request, 'webapp/index.html', context)


def services(request):
    item = get_object_or_404(ItemObject, pk=1)
    items = ItemObject.objects.prefetch_related('photos').distinct()
    # Получаем фотографии для item (ItemObject)
    photos = item.photos.all()

    context = {
        'item': item,
        'items': items,
        'photos': photos,
    }
    return render(request, 'webapp/services.html', context=context)

def single_services(request):
    return render(request, 'webapp/single_services.html')
