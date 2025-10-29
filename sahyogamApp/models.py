import os
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta
# ----------------------------
# Organization Model
# ----------------------------
class Organization(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    about = models.CharField(max_length=500,blank=True,null=True)
    org_type = models.CharField(max_length=50, choices=[
        ('NGO', 'NGO'),
        ('Research Group', 'Research Group'),
        ('Education Institute', 'Education Institute'),
        ('Charity', 'Charity'),
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
        return self.name or self.email


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
    start_time = models.CharField(max_length=100, blank=True, null=True)  
    end_time = models.CharField(max_length=100, blank=True, null=True)  
    banner_image = models.ImageField(upload_to="static/campaign_banners/", blank=True, null=True)  
    additional_instructions = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  
    postedBy = models.CharField(max_length=200)  
    organizationID = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class InviteCampaing(models.Model):
    title = models.CharField(max_length=300)
    short_description = models.CharField(max_length=300)  
    full_description = models.TextField()  
    skills_required = models.CharField(max_length=200) 
    location = models.CharField(max_length=200)  
    message = models.CharField(max_length=500)
    start_date = models.DateField()  
    end_date = models.DateField()  
    start_time = models.CharField(max_length=100, blank=True, null=True)  
    end_time = models.CharField(max_length=100, blank=True, null=True) 
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')  
    certificate_approved = models.BooleanField(default=False)
    OrganizationID = models.ForeignKey(Organization, on_delete=models.CASCADE)
    VolunteerID = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    

class AppliedCampaign(models.Model):
    
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    campaign =  models.ForeignKey(Campaign, on_delete=models.CASCADE)
    applied_at = models.CharField(max_length=100, blank=True, null=True)  
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')  # optional: track status of application

    certificate_approved = models.BooleanField(default=False)

    
    def __str__(self):
        return f"{self.applied_at}"
    
    
    

class Certificate(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, blank=True, null=True)
    invite_campaign = models.ForeignKey(InviteCampaing, on_delete=models.CASCADE, blank=True, null=True)
    issue_date = models.DateField(auto_now_add=True)
    certificate_file = models.FileField(upload_to='static/certificates/', blank=True, null=True)

   
    def __str__(self):
        title = self.campaign.title if self.campaign else self.invite_campaign.title
        return f"{self.volunteer.name} - {title}"

    def generate_pdf(self):
        """
        Generates a certificate PDF and saves it to self.pdf_file.
        """
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import Paragraph, Frame
        from reportlab.lib.styles import getSampleStyleSheet

        # Ensure certificates folder exists
        cert_dir = os.path.join(settings.MEDIA_ROOT, 'certificates')
        os.makedirs(cert_dir, exist_ok=True)

        file_path = os.path.join(cert_dir, f"certificate_{self.volunteer.name}_{self.id}.pdf")

        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        # Border
        c.setStrokeColor(HexColor("#0D47A1"))
        c.setLineWidth(4)
        c.rect(30, 30, width - 60, height - 60)

        # Title
        c.setFont("Helvetica-Bold", 28)
        c.setFillColor(HexColor("#0D47A1"))
        c.drawCentredString(width / 2, height - 120, "CERTIFICATE")

        # Body text
        c.setFont("Helvetica", 14)
        c.setFillColor(HexColor("#000000"))

        org_name = self.organization.name
        camp_title = self.campaign.title if self.campaign else self.invite_campaign.title

        text = (
            f"This is to certify that {self.volunteer.name}, "
            f"for donating their valuable skill(s): {self.volunteer.skills}, "
            f"has successfully participated in the campaign "
            f"\"{camp_title}\" organized by {org_name}."
        )

        styles = getSampleStyleSheet()
        style = styles["Normal"]
        style.fontSize = 14
        style.leading = 20

        p = Paragraph(text, style)
        frame = Frame(80, height / 2 - 60, width - 160, 120, showBoundary=0)
        frame.addFromList([p], c)

        # Footer
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, 120, "With warm regards,")
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width / 2, 90, org_name)

        c.showPage()
        c.save()

        # Save file path to model
        relative_path = f"certificates/certificate_{self.volunteer.name}_{self.id}.pdf"
        self.certificate_file.name = relative_path
        self.save()