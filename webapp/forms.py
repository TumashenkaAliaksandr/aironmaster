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
