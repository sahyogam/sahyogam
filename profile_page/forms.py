# profile_page/forms.py

from django import forms
from .models import VolunteerProfile, OrganizationProfile

class VolunteerProfileForm(forms.ModelForm):
    class Meta:
        model = VolunteerProfile
        fields = ['profile_photo', 'latitude', 'longitude']

class OrganizationProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizationProfile
        fields = ['profile_photo', 'latitude', 'longitude']
