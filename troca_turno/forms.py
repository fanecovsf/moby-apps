from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MobyUser

class MobyUserCreationForm(UserCreationForm):
    class Meta:
        model = MobyUser
        fields = ("email", "username", "password1", "password2", "operacao", "gestor")

    def save(self, commit=True):
        user = super(MobyUserCreationForm, self).save(commit=False)

        if commit:
            user.save()
        return user

class MobyUserChangeForm(forms.ModelForm):
    class Meta:
        model = MobyUser
        fields = '__all__'