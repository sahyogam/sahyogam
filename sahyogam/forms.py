from django import forms
from .models import Organization, Volunteer

class OrgForm(forms.ModelForm):
    class Meta:
        model = Organization
        exclude = []

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        exclude = []
