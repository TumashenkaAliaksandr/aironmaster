from .models import HadContact, FooterInfo, OurService


def had_contact_info(request):
    had_contact = HadContact.objects.first()
    footer_info = FooterInfo.objects.first()
    services = OurService.objects.all()  # Получаем все сервисы для меню
    return {
        'had_contact': had_contact,
        'footer_info': footer_info,
        'services': services,  # Добавляем сервисы в контекст
    }
