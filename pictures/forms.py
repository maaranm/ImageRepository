from django import forms
from .models import image

#form used for uploading the image and naming it
class image_form(forms.ModelForm):
    class Meta:
        model = image
        fields = ('image_name', 'image')

#form used for searching for objects
class search_form(forms.Form):
	object_name = forms.CharField(label='Object to find', max_length=200)

