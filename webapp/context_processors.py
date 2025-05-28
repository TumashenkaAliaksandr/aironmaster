from .models import HadContact, FooterInfo


def had_contact_info(request):
    # Можно получить один объект Contact, например первый или последний
    had_contact = HadContact.objects.first()
    footer_info = FooterInfo.objects.first()
    return {'had_contact': had_contact, 'footer_info': footer_info}
