from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'postEmail', 'placeholder' : 'Email'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'name' : 'username', 'id' : 'id_username', 'placeholder' : 'Никнейм'}), label = "Никнейм")
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'name' : 'password1', 'id' : 'id_password1', 'placeholder' : 'Парола'}), label = "Парола")
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'name' : 'password2', 'id' : 'id_password2', 'placeholder' : 'Повторете паролата'}), label = "Повторете")

    field_order = ['email', 'username', 'password1', 'password2']
    
    class Meta:
        model = User
        fields = {'username', 'password1', 'email', 'password2'}
        

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']

        if commit:
            user.save()
            print("yes")

        return user