
from django.urls import path
from . import views

urlpatterns = [
    path('', views.registrations, name="registration"),
    path('about/', views.about, name="about"),
    path('chpan/', views.pan_form, name='pan_form'),
    # path('volunteer/profile/<int:volunteer_id>/', views.volunteer_profile, name="volunteer_profile"),
    # path('organization/profile/<int:org_id>/', views.organization_profile, name="organization_profile"),
]
