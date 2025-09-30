import smtplib

from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator

from aironmaster import settings
from webapp.forms import ContactForm
from webapp.models import ItemObject, Banner, ServicesContact, About, OurService, BannerPage, News, Advertisement, \
    OurWorks
from webapp.utils import handle_order_form

from django.conf import settings

def index(request):
    order_form, order_error, order_success = handle_order_form(request)
    news_list = News.objects.all()[:10]

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
                text_content = (
                    f"Имя: {cd['name']}\n"
                    f"Телефон: {cd['phone']}\n"
                    f"Email: {cd['email']}\n"
                    f"Сообщение:\n{cd['message']}"
                )
                try:
                    # Отправляем на ваш email (можно добавить еще адреса в список)
                    email = EmailMultiAlternatives(
                        subject,
                        text_content,
                        'Aironmaster <tumashenkaaliaksandr@gmail.com>',
                        ['aironmaster@tut.by', 'Badminton500@inbox.lv']
                    )
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
    items = ItemObject.objects.filter(is_main=True).prefetch_related('photos').distinct()
    services_info = ServicesContact.objects.all()
    banner = get_object_or_404(Banner, pk=1)
    about = About.objects.first()
    photose = []
    for i in range(1, 5):
        photo = getattr(banner, f'photo{i}')
        description = getattr(banner, f'photo{i}_description')
        link = getattr(banner, f'photo{i}_link', '')
        if photo and hasattr(photo, 'url'):
            photose.append({
                'photo_url': photo.url,
                'description': description,
                'link': link,
            })

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
        'news_list': news_list,
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
    CATEGORY_MAP = {
        'metal_structures': 'is_metal_structures',
        'procladki': 'is_prokladki_mtgr',
        'steps_and_stairs': 'is_steps_and_stairs',
        'grills': 'is_grills',
        'decor_elements': 'is_decor_elements',
    }

    selected_category = request.GET.get('category')

    items = ItemObject.objects.prefetch_related('photos').distinct()

    if selected_category in CATEGORY_MAP:
        filter_field = CATEGORY_MAP[selected_category]
        filter_kwargs = {filter_field: True}
        items = items.filter(**filter_kwargs)

    item = get_object_or_404(ItemObject, pk=1)
    photos = item.photos.all()

    context = {
        'item': item,
        'items': items,
        'photos': photos,
        'categories': {
            'metal_structures': 'Металлоконструкции',
            'procladki': 'Прокладки',
            'steps_and_stairs': 'Ступени и лестницы',
            'grills': 'Решётки',
            'decor_elements': 'Декоративные элементы',
        },
        'selected_category': selected_category,
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
    photos = service.photos.all()  # related_name='photos'

    services_info = ServicesContact.objects.all()
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
                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    'Aironmaster <tumashenkaaliaksandr@gmail.com>',
                    ['aironmaster@tut.by', 'Badminton500@inbox.lv']
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
            except (smtplib.SMTPException, BadHeaderError):
                error_message = "Ошибка при отправке письма. Пожалуйста, попробуйте позже."
            else:
                return render(request, 'webapp/contact_success.html')
    else:
        form = ContactForm()

    context = {
        'service': service,
        'photos': photos,
        'error_message': error_message,
        'services_info': services_info,
        'form': form,
    }

    return render(request, 'webapp/service_detail.html', context=context)


def single_services(request):
    return render(request, 'webapp/single_services.html')

def about(request):
    about = About.objects.first()
    advertisement = get_object_or_404(Advertisement, id=1)  # измените id под ваш случай
    works = OurWorks.objects.all()
    # Формируем ads для динамической рекламы из других объявлений, например, кроме текущего
    ads = Advertisement.objects.exclude(id=advertisement.id)

    context = {
        'about': about,
        'works': works,
        'ads': ads,
        'advertisement': advertisement,
    }
    return render(request, 'webapp/about.html', context=context)

def contacts(request):
    services_info = ServicesContact.objects.all()
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
                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    'Aironmaster <tumashenkaaliaksandr@gmail.com>',
                    ['aironmaster@tut.by', 'Badminton500@inbox.lv']
                )
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
        'services_info': services_info,
    })


def item_detail(request, slug):
    item = get_object_or_404(ItemObject, slug=slug)
    photos = item.photos.all()

    # Формируем фильтр по категориям (булевым полям)
    category_filter = Q()
    if item.is_metal_structures:
        category_filter |= Q(is_metal_structures=True)
    if item.is_prokladki_mtgr:
        category_filter |= Q(is_prokladki_mtgr=True)
    if item.is_steps_and_stairs:
        category_filter |= Q(is_steps_and_stairs=True)
    if item.is_grills:
        category_filter |= Q(is_grills=True)
    if item.is_decor_elements:
        category_filter |= Q(is_decor_elements=True)

    # Получаем похожие изделия из тех же категорий, исключая текущее
    items = ItemObject.objects.filter(category_filter).exclude(id=item.id).prefetch_related('photos').distinct()

    services_info = ServicesContact.objects.all()
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
                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    'Aironmaster <tumashenkaaliaksandr@gmail.com>',
                    ['aironmaster@tut.by', 'Badminton500@inbox.lv']
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
            except (smtplib.SMTPException, BadHeaderError):
                error_message = "Ошибка при отправке письма. Пожалуйста, попробуйте позже."
            else:
                return render(request, 'webapp/contact_success.html')
    else:
        form = ContactForm()

    context = {
        'item': item,
        'items': items,
        'photos': photos,
        'form': form,
        'error_message': error_message,
        'services_info': services_info,
    }
    return render(request, 'webapp/item_detail.html', context)


def news_list(request):
    news_queryset = News.objects.all().order_by('-date')
    paginator = Paginator(news_queryset, 10)

    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('webapp/news_items.html', {'news_list': page_obj.object_list})
        return JsonResponse({'html': html, 'has_next': page_obj.has_next()})

    return render(request, 'webapp/news_list.html', {'news_list': page_obj.object_list, 'page_obj': page_obj})

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    news_list = News.objects.all()[:10]
    return render(request, 'webapp/news_detail.html', {'news': news, 'news_list': news_list})


def advertisement(request):
    """ Advertisement page """
    # Можно взять конкретное объявление, например с id=1,
    # либо первое в базе (если у вас всего одно)
    advertisement = get_object_or_404(Advertisement, id=1)  # измените id под ваш случай
    works = OurWorks.objects.all()
    # Формируем ads для динамической рекламы из других объявлений, например, кроме текущего
    ads = Advertisement.objects.exclude(id=advertisement.id)

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
                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    'Aironmaster <tumashenkaaliaksandr@gmail.com>',
                    ['aironmaster@tut.by', 'Badminton500@inbox.lv']
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
            except (smtplib.SMTPException, BadHeaderError):
                error_message = "Ошибка при отправке письма. Пожалуйста, попробуйте позже."
            else:
                return render(request, 'webapp/contact_success.html')
    else:
        form = ContactForm()

    context = {
        'advertisement': advertisement,
        'ads': ads,
        'error_message': error_message,
        'form': form,
        'works': works,
    }

    return render(request, 'webapp/advertisement.html', context=context)


def sitemap_view(request):

    # Для продакшена (глобального хоста) используйте фиксированный URL:
    base_url = 'https://aironmaster.by'  # <=== раскомментируйте этот URL при деплое
    # base_url = request.build_absolute_uri('/').rstrip('/')  # <=== закомментируйте этот при деплое

    urls = [
        {'location': base_url + reverse('index'), 'lastmod': timezone.now().date()},
        {'location': base_url + reverse('about'), 'lastmod': timezone.now().date()},
        {'location': base_url + reverse('products'), 'lastmod': timezone.now().date()},
        {'location': base_url + reverse('single-services'), 'lastmod': timezone.now().date()},
        {'location': base_url + reverse('contacts'), 'lastmod': timezone.now().date()},
        {'location': base_url + reverse('sitemap'), 'lastmod': timezone.now().date()},
    ]

    categories = ['metal_structures', 'procladki', 'steps_and_stairs', 'grills', 'decor_elements']

    item_slugs = ItemObject.objects.filter(slug__isnull=False).values_list('slug', flat=True)
    service_slugs = OurService.objects.filter(slug__isnull=False).values_list('slug', flat=True)

    for category in categories:
        url = base_url + reverse('products_by_category', kwargs={'category': category})
        urls.append({'location': url, 'lastmod': timezone.now().date()})

    for slug in item_slugs:
        url = base_url + reverse('item_detail', kwargs={'slug': slug})
        urls.append({'location': url, 'lastmod': timezone.now().date()})

    for slug in service_slugs:
        url = base_url + reverse('service_detail', kwargs={'slug': slug})
        urls.append({'location': url, 'lastmod': timezone.now().date()})

    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{url["location"]}</loc>\n'
        xml_content += f'    <lastmod>{url["lastmod"].isoformat()}</lastmod>\n'
        xml_content += '    <changefreq>weekly</changefreq>\n'
        xml_content += '    <priority>0.8</priority>\n'
        xml_content += '  </url>\n'

    xml_content += '</urlset>'

    return HttpResponse(xml_content, content_type='application/xml')




def robots_txt(request):
    # sitemap_url = request.build_absolute_uri('/sitemap.xml')  # для локали
    sitemap_url = "https://aironmaster.by/sitemap.xml"  # для продакшена

    content = render_to_string("robots.txt", {"sitemap_url": sitemap_url})
    return HttpResponse(content, content_type="text/plain")


@require_GET
def ajax_search(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        # Поиск по сервисам
        services = OurService.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()[:10]

        for service in services:
            url = getattr(service, 'get_absolute_url', None)
            results.append({
                'type': 'service',
                'title': service.name,
                'url': url() if callable(url) else f"/service/{service.slug}/",
                'description': (service.description[:197] + '...') if service.description and len(service.description) > 200 else (service.description or ''),
            })

        # Поиск по изделиям
        items = ItemObject.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(description_more__icontains=query) |
            Q(phone1__icontains=query) |
            Q(phone2__icontains=query) |
            Q(service__name__icontains=query)
        ).distinct()[:10]

        for item in items:
            url = getattr(item, 'get_absolute_url', None)
            results.append({
                'type': 'item',
                'title': item.name,
                'url': url() if callable(url) else f"/item/{item.slug}/",
                'description': (item.description[:197] + '...') if item.description and len(item.description) > 200 else (item.description or ''),
            })

        # Поиск по новостям
        news_results = News.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(news_text__icontains=query)
        ).order_by('-date')[:10]

        for news in news_results:
            url = getattr(news, 'get_absolute_url', None)
            results.append({
                'type': 'news',
                'title': news.name,
                'url': url() if callable(url) else f"/news/{news.slug}/",
                'description': (news.description[:197] + '...') if news.description and len(news.description) > 200 else (news.description or ''),
            })

    return JsonResponse({'results': results})
