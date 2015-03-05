from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.fields.TextInput(attrs={
                'placeholder': 'Enter username',
                'class': 'form-control',
                }),
            'email': forms.fields.TextInput(attrs={
                'placeholder': 'Enter email',
                'class': 'form-control',
                }),
            'password1': forms.fields.TextInput(attrs={
                'placeholder': 'Enter password',
                'class': 'form-control',
                }),
            'password2': forms.fields.TextInput(attrs={
                'placeholder': 'Enter password again',
                'class': 'form-control',
                }),
        }

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            return user
