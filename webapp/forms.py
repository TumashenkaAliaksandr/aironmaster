from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Banner, OurService


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = '__all__'
        widgets = {
            'description': SummernoteWidget(),
            'photo1_description': forms.TextInput(attrs={'size': 40}),
            'photo2_description': forms.TextInput(attrs={'size': 40}),
            'photo3_description': forms.TextInput(attrs={'size': 40}),
            'photo4_description': forms.TextInput(attrs={'size': 40}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(
        label='Имя',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя', 'required': True})
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': '+375 (__) ___-__-__',
            'pattern': r'^\+?\d{7,15}$',
            'required': True
        })
    )
    email = forms.EmailField(
        label='Почта',
        widget=forms.EmailInput(attrs={'placeholder': 'aironmaster@tut.by', 'required': True})
    )
    message = forms.CharField(
        label='Описание',
        widget=forms.Textarea(attrs={'placeholder': 'Ваше сообщение', 'rows': 4})
    )



class OrderForm(forms.Form):
    type = forms.ChoiceField(label='Тип', choices=[
        ('', 'не выбрано'),
        ('труба', 'труба'),
        ('желоб', 'желоб'),
        ('другой', 'другой'),
    ], required=True)
    voltage = forms.ChoiceField(label='Напряжение', choices=[
        ('', 'не выбрано'),
        ('220', '220'),
        ('330', '330'),
    ], required=False)
    drive = forms.ChoiceField(label='Привод', choices=[
        ('', 'не выбрано'),
        ('справа', 'справа'),
        ('слева', 'слева'),
        ('другое', 'другое'),
    ], required=False)
    material = forms.ChoiceField(label='Материал', choices=[
        ('', 'не выбрано'),
        ('сталь', 'сталь'),
        ('оцинковка', 'оцинковка'),
        ('нержавейка', 'нержавейка'),
        ('алюминий', 'алюминий'),
    ], required=False)
    performance = forms.CharField(label='Производительность', required=False)
    cargo = forms.CharField(label='Характеристика груза', required=False)
    weight = forms.CharField(label='Масса', required=False)
    diameter = forms.CharField(label='Диаметр винта', required=False)
    length = forms.CharField(label='Длина габаритная', required=False)
    height_start = forms.CharField(label='Высота начальная', required=False)
    height_end = forms.CharField(label='Высота конечная', required=False)
    speed = forms.CharField(label='Скорость', required=False)
    reductor = forms.CharField(label='Редуктор, тип, мощность', required=False)
    height_regulation = forms.CharField(label='Регулировка по высоте', required=False)
    quantity = forms.CharField(label='Количество (шт.)', required=False)
    name = forms.CharField(label='Имя', required=True)
    email = forms.EmailField(label='Email', required=True)
    phone = forms.CharField(label='Телефон', required=False)
    message = forms.CharField(label='Дополнительная информация', widget=forms.Textarea, required=False)


class OurServiceForm(forms.ModelForm):
    class Meta:
        model = OurService
        fields = '__all__'
        widgets = {
            'description': SummernoteWidget(),
        }