from django.shortcuts import render, get_object_or_404

from webapp.models import ItemObject


def index(request):
    item = get_object_or_404(ItemObject, pk=1)
    items = ItemObject.objects.prefetch_related('photos').distinct()

    photos = item.photos.all()  # связанные фотографии

    context = {
        'item': item,
        'photos': photos,
        'items': items,
    }
    return render(request, 'webapp/index.html', context)


def services(request):
    return render(request, 'webapp/services.html')

def single_services(request):
    return render(request, 'webapp/single_services.html')
