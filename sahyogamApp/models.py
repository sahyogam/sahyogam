from django.db import models
from django.utils import timezone
from datetime import timedelta
# ----------------------------
# Organization Model
# ----------------------------
class Organization(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, blank=True, null=True,unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    
    org_type = models.CharField(max_length=50, choices=[
        ('ngo', 'NGO'),
        ('research', 'Research Group'),
        ('education', 'Education Institute'),
        ('charity', 'Charity'),
    ])
    address = models.TextField()
    profile_photo = models.ImageField(upload_to='static/images/', null=True, blank=True)
    

    def __str__(self):
        return self.name


# Volunteer Model

class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, blank=True, null=True,unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    skills = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    # profile_photo = models.CharField(max_length=255, blank=True)
    profile_photo = models.ImageField(upload_to='static/images/', null=True, blank=True)


    def __str__(self):
        return self.username or self.email


# OTP Verification Model

class EmailOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=3)

    def __str__(self):
        return f"{self.email} - {self.otp}"



class Campaign(models.Model):
    title = models.CharField(max_length=200)  
    short_description = models.CharField(max_length=300)  
    full_description = models.TextField()  
    skills_required = models.CharField(max_length=200) 
    location = models.CharField(max_length=200)  
    total_volunteers_needed = models.PositiveIntegerField()  
    applied = models.PositiveIntegerField() 
    start_date = models.DateField()  
    end_date = models.DateField()  
    time_slot = models.CharField(max_length=100, blank=True, null=True)  
    banner_image = models.ImageField(upload_to="static/campaign_banners/", blank=True, null=True)  
    additional_instructions = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  
    postedBy = models.CharField(max_length=200)  

    def __str__(self):
        return self.title
