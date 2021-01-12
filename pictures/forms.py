from django import forms
from .models import Image


class image_form(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('caption', 'image')

