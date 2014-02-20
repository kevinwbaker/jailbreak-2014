from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate
from django.conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, ButtonHolder, Hidden, Row

class SignInBase(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(SignInBase, self).__init__(*args, **kwargs)

    def clean_email(self):
        '''Forces the email address to lowercase'''
        self.email = self.cleaned_data.get('email').lower()
        return self.email

    def _signin(self, email, password):
        '''Attempts to log the user in with the provided credentials'''
        user = auth_authenticate(username=email, password=password)
        if user:
            auth_login(self.request, user)
            return user
        else:
            raise forms.ValidationError(_("Incorrect email or password"))

    def clean(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(
                _("Your Web browser doesn't appear to have cookies enabled. "
                  "Cookies are required for logging in."))
        return self.cleaned_data

class EmailAuthenticationForm(SignInBase):

    def __init__(self, *args, **kwargs):
        super(EmailAuthenticationForm, self).__init__(*args, prefix='signin', **kwargs)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset("", Row('email', 'password')),
            ButtonHolder(Submit('submit', _("Sign In")))
        )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        self._signin(email, password)
        return self.cleaned_data

        