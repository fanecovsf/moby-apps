from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MobyUser

class MobyUserCreationForm(UserCreationForm):
    class Meta:
        model = MobyUser
        fields = ('email',)

class MobyUserChangeForm(forms.ModelForm):
    class Meta:
        model = MobyUser
        fields = '__all__'