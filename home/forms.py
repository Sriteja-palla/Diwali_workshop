from django import forms
from .models import Crackers, Sweets, Gifts
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField

class CrackerForm(forms.ModelForm):
    class Meta:
        model = Crackers
        fields = "__all__"

class SweetsForm(forms.ModelForm):
    class Meta:
        model = Sweets
        fields = "__all__"

class GiftsForm(forms.ModelForm):
    class Meta:
        model = Gifts
        fields = "__all__"

class CrackersForm(forms.ModelForm):
    class Meta:
        model = Crackers
        fields = "__all__"


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username' , 'email' , 'password1' , 'password2']

    def save(self ,commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit :
            user.save()
            return user


class RecaptchaForm(forms.Form):
    Captcha = ReCaptchaField()