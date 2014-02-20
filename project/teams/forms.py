from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate
from django.conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, ButtonHolder, Hidden

from teams.models import Team, Checkin

class EditTeamForm(forms.Form):
    name = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(EditTeamForm, self).__init__(*args, **kwargs)

    def save(self):
        pass

    def clean(self):
        pass
        

class CreateCheckinForm(forms.Form):
    message = forms.CharField(label="Checkin Message")
    lat = forms.CharField(label="Latitude", required=True)
    lng = forms.CharField(label="Longitude", required=False)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(EditTeamForm, self).__init__(*args, **kwargs)

        # dynamically generate a list of teams for the form
        teams = Team.objects.all()
        self.fields['team'] = forms.ChoiceField(label="Team", required=True, choices=[unicode(team) for team in teams])
        self.helper.add_input(Submit('submit', 'Add Campaign URL'))

    def save(self):
        pass

    def clean(self):
        pass
        