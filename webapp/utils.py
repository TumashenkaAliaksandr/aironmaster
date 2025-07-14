from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.template.loader import render_to_string
from django.conf import settings
import smtplib

from webapp.forms import OrderForm  # импорт вашей формы заказа

def handle_order_form(request):
    error_message = None
    if request.method == 'POST' and 'order_submit' in request.POST:
        form = OrderForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = 'Новый заказ шнека с сайта'
            context_email = {
                'type': cd.get('type', ''),
                'voltage': cd.get('voltage', ''),
                'drive': cd.get('drive', ''),
                'material': cd.get('material', ''),
                'performance': cd.get('performance', ''),
                'cargo': cd.get('cargo', ''),
                'weight': cd.get('weight', ''),
                'diameter': cd.get('diameter', ''),
                'length': cd.get('length', ''),
                'height_start': cd.get('height_start', ''),
                'height_end': cd.get('height_end', ''),
                'speed': cd.get('speed', ''),
                'reductor': cd.get('reductor', ''),
                'height_regulation': cd.get('height_regulation', ''),
                'quantity': cd.get('quantity', ''),
                'name': cd.get('name', ''),
                'email': cd.get('email', ''),
                'phone': cd.get('phone', ''),
                'message': cd.get('message', ''),
            }
            html_content = render_to_string('webapp/email/order_email.html', context_email)
            text_content = '\n'.join([f"{key}: {value}" for key, value in context_email.items()])
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
                error_message = "Ошибка при отправке заказа. Пожалуйста, попробуйте позже."
            else:
                return form, None, True
        else:
            return form, None, False
    else:
        form = OrderForm()
    return form, None, False
