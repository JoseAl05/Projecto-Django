from django import forms
from core.user.models import User


class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter your username',
            'class': 'form-control',
            'autocomplete': 'off'
        }
    ))

    def clean(self):
        cleaned = super().clean()

        if not User.objects.filter(username=cleaned['username']).exists():
            self._errors['error'] = self._errors.get('error', self.error_class())
            self._errors['error'].append('User does not exists')
            #raise forms.ValidationError('User does not exists')
        return cleaned

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Enter your password',
            'class': 'form-control',
            'autocomplete': 'off'
        }
    ))

    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Confirm your password',
            'class': 'form-control',
            'autocomplete': 'off'
        }
    ))


    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirm_password = cleaned['confirm_password']

        if password != confirm_password:
            self._errors['error'] = self._errors.get('error', self.error_class())
            self._errors['error'].append('Passwords must be the same')
            #raise forms.ValidationError('User does not exists')
        return cleaned

    # def get_user(self):
    #     username = self.cleaned_data.get('username')
    #     return User.objects.get(username=username)
