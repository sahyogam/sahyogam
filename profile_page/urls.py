from django.urls import path
from . import views

urlpatterns = [
    path('organization/<int:org_id>/', views.organization_profile_page, name='organization_profile_page'),
    path('organization/<int:org_id>/delete-photo/', views.delete_org_photo, name='delete_org_photo'),

    path('volunteer/<int:vol_id>/', views.volunteer_profile_page, name='volunteer_profile_page'),
    path('volunteer/<int:vol_id>/delete-photo/', views.delete_vol_photo, name='delete_vol_photo'),
]
