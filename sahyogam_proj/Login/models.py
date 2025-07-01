from django.db import models

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50, unique=True)
    org_type = models.CharField(max_length=50)  # e.g., Temple, NGO, School
    established_year = models.PositiveIntegerField()
    
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    
    registered_doc = models.FileField(upload_to='org_documents/')
    agree_to_terms = models.BooleanField(default=False)

    def __str__(self):
        return self.name




class Volunteer(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()

    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    skill = models.CharField(max_length=100)  # e.g., Carpenter, Teacher
    experience_years = models.PositiveIntegerField()

    availability = models.CharField(max_length=100)
    consent_public = models.BooleanField(default=True)
    agree_to_terms = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name



# class SkillAssignment(models.Model):
#     # Organization info
#     organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
#     # Task details
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     skill_needed = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)
#     date_posted = models.DateTimeField(auto_now_add=True)

#     # Volunteer who applied or was assigned
#     volunteer = models.ForeignKey(Volunteer, on_delete=models.SET_NULL, null=True, blank=True)

#     # Application status
#     status = models.CharField(max_length=20, choices=[
#         ('open', 'Open for Application'),
#         ('applied', 'Volunteer Applied'),
#         ('assigned', 'Volunteer Assigned'),
#         ('completed', 'Completed'),
#     ], default='open')

#     # Timestamps
#     applied_date = models.DateTimeField(null=True, blank=True)
#     assigned_date = models.DateTimeField(null=True, blank=True)
#     completed_date = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.title} ({self.skill_needed}) - {self.status}"
