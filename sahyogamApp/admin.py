from django.contrib import admin
from .models import Organization, Volunteer,Campaign,AppliedCampaign

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone','get_org_type')
    search_fields = ('name', 'email')
    list_filter = ('org_type',)
    
    def get_org_type(self, obj):
        return obj.get_org_type_display()  
    get_org_type.short_description = 'Organization Type'

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title','postedBy','start_date','end_date','start_time','end_time','skills_required','location','total_volunteers_needed')
    search_fields = ('title','short_description','skills_required')
    
from django.contrib import admin
from .models import AppliedCampaign

@admin.register(AppliedCampaign)
class AppliedCampaignAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'campaign', 'applied_at', 'status','certificate_approved')
    search_fields = ('volunteer__name', 'campaign__title')
    list_filter = ('status', 'applied_at')
