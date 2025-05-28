from .models import HadContact


def had_contact_info(request):
    # Можно получить один объект Contact, например первый или последний
    had_contact = HadContact.objects.first()
    return {'had_contact': had_contact}
