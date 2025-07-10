from django.urls import path
from . import views  # importing from registration app

urlpatterns = [
    path('profile/<int:org_id>/', views.organization_profile, name="organization_profile"),
]
