from django.contrib import admin
from .models import Organization, Volunteer,Campaign

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'org_type')
    search_fields = ('name', 'email')
    list_filter = ('org_type',)

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title','postedBy','skills_required','location','total_volunteers_needed')
    search_fields = ('title','short_description','skills_required')
    
    