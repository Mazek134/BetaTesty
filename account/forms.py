from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class MyLoginForm(AuthenticationForm):

    # do nadpisania formluarza logowania z gotowca django
    def __init__(self, request, *args, **kwargs):

         super().__init__(*args, **kwargs)

    username = forms.CharField(label='',widget=forms.Textarea(attrs={'rows': 2, 'cols': 50}))
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'size': 48}))
    username.widget.attrs.update({'class': 'usernameField','placeholder':'username'})
    password.widget.attrs.update({'class': 'passwordField','placeholder':'password'})

    # wlasny formularz musi miec authenticate uzytkownika
    def get_user(self):
        from django.contrib.auth import authenticate
        return authenticate(
            username=self.cleaned_data.get('username', '').lower().strip(),
            password=self.cleaned_data.get('password', ''),
        )

class UserRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password', 'password2']:
            self.fields[fieldname].help_text = None

    password = forms.CharField(label='',widget=forms.PasswordInput)
    password2 = forms.CharField(label='', widget=forms.PasswordInput)
    password.widget.attrs.update({'class': 'passwordFieldinRegister', 'placeholder': 'password'})
    password2.widget.attrs.update({'class': 'passwordFieldinRegister', 'placeholder': 'password2'})
    class Meta:
        model = User
        fields = ('username','first_name','email')
        labels = {
            'username': "",
            'first_name':"",
            'email':""
        }
        widgets = {'username': forms.Textarea(attrs={'class':'usernameFieldinRegister','placeholder':'twoj nick' }),
                   'first_name': forms.Textarea(attrs={'class': 'first_nameFieldinRegister','placeholder':'imię'}),
                   'email': forms.Textarea(attrs={'class': 'mailFieldinRegister','placeholder':'adres e-mail'})
                   }
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('hasła nie sa identyczne')
        return cd['password2']

