# profile_page/models.py

from django.db import models
from Registration.models import Volunteer, Organization

class VolunteerProfile(models.Model):
    volunteer = models.OneToOneField(Volunteer, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='volunteer/', blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

class OrganizationProfile(models.Model):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='organization/', blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
