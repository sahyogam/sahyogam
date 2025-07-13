from django.db import models

# Create your models here.


# Create your models here.
class Organization(models.Model):
    org_name = models.CharField(max_length=100)
    org_reg_number = models.CharField(max_length=50, unique=True)
    org_type = models.CharField(max_length=50)  # e.g., Temple, NGO, School
    org_established_yer = models.PositiveIntegerField()
    
    org_address = models.TextField()
    org_city = models.CharField(max_length=50)
    org_state = models.CharField(max_length=50)
    org_country = models.CharField(max_length=50)
    org_pincode = models.CharField(max_length=10)
    
    org_contact_person = models.CharField(max_length=100)
    org_contact_email = models.EmailField()
    org_contact_phone = models.CharField(max_length=15)
    
    org_registered_doc = models.FileField(upload_to='org_documents/')
    org_agree_to_terms = models.BooleanField(default=False)

    def __str__(self):
        return self.org_name




class Volunteer(models.Model):
    volunteer_fname = models.CharField(max_length=100)
    volunteer_email = models.EmailField(unique=True)
    volunteer_phno = models.CharField(max_length=15, unique=True)
    volunteer_dob = models.DateField()

    volunteer_city = models.CharField(max_length=50)
    volunteer_state = models.CharField(max_length=50)
    volunteer_pincode = models.CharField(max_length=10)

    volunteer_skill = models.CharField(max_length=100)  # e.g., Carpenter, Teacher
    volunteer_experience_years = models.PositiveIntegerField()

    volunteer_availability = models.CharField(max_length=100)
    volunteer_consent_public = models.BooleanField(default=True)
    volunteer_agree_to_terms = models.BooleanField(default=False)

    def __str__(self):
        return self.volunteer_fname



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
