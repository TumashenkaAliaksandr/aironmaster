from django.shortcuts import render, get_object_or_404

from webapp.models import ItemObject, Banner, ServicesContact, About, OurService, BannerPage


def index(request):
    item = get_object_or_404(ItemObject, pk=1)
    items = ItemObject.objects.prefetch_related('photos').distinct()
    services_info = ServicesContact.objects.all()

    # Получаем баннер с id=1
    banner = get_object_or_404(Banner, pk=1)
    about = About.objects.first()

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
        'services_info': services_info,
        'about': about,
    }
    return render(request, 'webapp/index.html', context)

# Словарь соответствия категории из URL и поля модели
CATEGORY_MAP = {
    'metal_structures': 'is_metal_structures',
    'steps_and_stairs': 'is_steps_and_stairs',
    'grills': 'is_grills',
    'decor_elements': 'is_decor_elements',
}

def products(request):
    item = get_object_or_404(ItemObject, pk=1)
    items = ItemObject.objects.prefetch_related('photos').distinct()
    # Получаем фотографии для item (ItemObject)
    photos = item.photos.all()

    context = {
        'item': item,
        'items': items,
        'photos': photos,
    }
    return render(request, 'webapp/products.html', context=context)


def products_by_done(request, category):
    banner = BannerPage.objects.filter(category=category).first()
    field_name = CATEGORY_MAP.get(category)
    if not field_name:
        # Если категория не найдена, можно вернуть 404 или все изделия
        items = ItemObject.objects.none()
    else:
        # Фильтруем изделия, где соответствующее булево поле True
        filter_kwargs = {field_name: True}
        items = ItemObject.objects.filter(**filter_kwargs)

    # Для отображения названия категории на странице
    category_verbose = {
        'metal_structures': 'Металлоконструкции',
        'steps_and_stairs': 'Ступеньки и Лестницы',
        'grills': 'Мангалы',
        'decor_elements': 'Элементы декора',
    }.get(category, '')

    context = {
        'items': items,
        'category_name': category_verbose,
        'banner': banner,
    }
    return render(request, 'webapp/single_products.html', context)


def item_detail(request, slug):
    item = get_object_or_404(ItemObject, slug=slug)
    return render(request, 'webapp/single_products.html', {'item': item})

def service_detail(request, slug):
    service = get_object_or_404(OurService, slug=slug)
    return render(request, 'webapp/service_detail.html', {'service': service})

def single_services(request):
    return render(request, 'webapp/single_services.html')

def about(request):
    about = About.objects.first()

    context = {
        'about': about,
    }
    return render(request, 'webapp/about.html', context=context)

def contacts(request):
    return render(request, 'webapp/contacts.html')
