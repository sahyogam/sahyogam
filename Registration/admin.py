from django.contrib import admin
from .models import Volunteer,Organization
# Register your models here.


admin.site.site_header = "Sahyogam Admin"
admin.site.site_title = "Sahyogam Admin Portal"
admin.site.index_title = "Welcome to Sahyogam Dashboard"

admin.site.register(Organization)
admin.site.register(Volunteer)