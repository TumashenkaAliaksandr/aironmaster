from .models import HadContact, FooterInfo, OurService, Banner


def had_contact_info(request):
    had_contact = HadContact.objects.first()
    footer_info = FooterInfo.objects.first()
    services = OurService.objects.all()  # Получаем все сервисы для меню
    return {
        'had_contact': had_contact,
        'footer_info': footer_info,
        'services': services,  # Добавляем сервисы в контекст
    }



def banners_photos(request):
    photose = []
    try:
        banner = Banner.objects.get(pk=1)  # или фильтр по нужному условию
        for i in range(1, 5):
            photo = getattr(banner, f'photo{i}')
            description = getattr(banner, f'photo{i}_description')
            link = getattr(banner, f'photo{i}_link', '')  # ссылка, если есть
            if photo:
                photose.append({
                    'photo': photo,
                    'description': description,
                    'link': link,
                })
    except Banner.DoesNotExist:
        photose = []
    return {
        'photose': photose
    }

