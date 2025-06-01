from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Banner


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


from django import forms

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
        widget=forms.EmailInput(attrs={'placeholder': 'example@mail.com', 'required': True})
    )
    message = forms.CharField(
        label='Описание',
        widget=forms.Textarea(attrs={'placeholder': 'Ваше сообщение', 'rows': 4})
    )


