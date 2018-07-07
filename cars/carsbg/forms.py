from django import forms

class ImageForm(forms.Form):
	imgfile = forms.ImageField(label = 'Choose your image', help_text = 'The image should be cool.')