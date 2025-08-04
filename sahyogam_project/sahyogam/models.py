from django.db import models

# ----------------------------
# Organization Model
# ----------------------------
class Organization(models.Model):
    name = models.CharField(max_length=100)
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

    def __str__(self):
        return self.name

# ----------------------------
# Volunteer Model
# ----------------------------
class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    skills = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username or self.email

# ----------------------------
# OTP Verification Model
# ----------------------------
class OTPVerification(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.otp}"
