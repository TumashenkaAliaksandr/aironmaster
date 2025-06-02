import smtplib

from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from aironmaster import settings
from webapp.forms import ContactForm
from webapp.models import ItemObject, Banner, ServicesContact, About, OurService, BannerPage
from webapp.utils import handle_order_form


def index(request):
    order_form, order_error, order_success = handle_order_form(request)

    error_message = None
    contact_success = False

    if request.method == 'POST':
        if 'contact_submit' in request.POST:
            form = ContactForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                subject = 'Новое сообщение с сайта'
                context_email = {
                    'name': cd['name'],
                    'phone': cd['phone'],
                    'email': cd['email'],
                    'message': cd['message'],
                }
                html_content = render_to_string('webapp/email_template.html', context_email)
                text_content = f"""
                Имя: {cd['name']}
                Телефон: {cd['phone']}
                Email: {cd['email']}
                Сообщение:
                {cd['message']}
                """
                try:
                    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
                    email.attach_alternative(html_content, "text/html")
                    email.send()
                except (smtplib.SMTPException, BadHeaderError):
                    error_message = "Ошибка при отправке письма. Пожалуйста, попробуйте позже."
                else:
                    contact_success = True
            else:
                form = ContactForm(request.POST)
        elif 'order_submit' in request.POST:
            # Форма заказа уже обработана в handle_order_form
            form = ContactForm()  # пустая форма обратной связи
            if order_success:
                return render(request, 'webapp/contact_success.html')
        else:
            form = ContactForm()
    else:
        form = ContactForm()

    # Остальной код для контекста
    item = get_object_or_404(ItemObject, pk=1)
    items = ItemObject.objects.prefetch_related('photos').distinct()
    services_info = ServicesContact.objects.all()
    banner = get_object_or_404(Banner, pk=1)
    about = About.objects.first()
    photose = []
    for i in range(1, 5):
        photo = getattr(banner, f'photo{i}')
        description = getattr(banner, f'photo{i}_description')
        if photo:
            photose.append({'photo': photo, 'description': description})
    photos = item.photos.all()

    context = {
        'form': form,
        'order_form': order_form,
        'error_message': error_message,
        'order_error': order_error,
        'contact_success': contact_success,
        'item': item,
        'items': items,
        'photos': photos,
        'banner': [banner],
        'photose': photose,
        'services_info': services_info,
        'about': about,
    }

    if contact_success:
        return render(request, 'webapp/contact_success.html')

    return render(request, 'webapp/index.html', context)


# Словарь соответствия категории из URL и поля модели
CATEGORY_MAP = {
    'metal_structures': 'is_metal_structures',
    'procladki': 'is_prokladki_mtgr',
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
        'procladki': 'Прокладки',
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


def item_details(request, slug):
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
    error_message = None
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = 'Новое сообщение с контактов сайта'
            context_email = {
                'name': cd['name'],
                'phone': cd['phone'],
                'email': cd['email'],
                'message': cd['message'],
            }
            html_content = render_to_string('webapp/email_template.html', context_email)
            text_content = f"""
            Имя: {cd['name']}
            Телефон: {cd['phone']}
            Email: {cd['email']}
            Сообщение:
            {cd['message']}
            """
            try:
                email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
                email.attach_alternative(html_content, "text/html")
                email.send()
            except (smtplib.SMTPException, BadHeaderError):
                error_message = "Ошибка при отправке письма. Пожалуйста, попробуйте позже."
            else:
                return render(request, 'webapp/contact_success.html')
    else:
        form = ContactForm()

    return render(request, 'webapp/contacts.html', {
        'form': form,
        'error_message': error_message,
    })


def item_detail(request, slug):
    item = get_object_or_404(ItemObject, slug=slug)
    context = {
        'item': item,
    }
    return render(request, 'webapp/item_detail.html', context)
