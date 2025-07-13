from django.urls import path
from . import views

urlpatterns = [
    path("profile/<int:vol_id>/",views.volunteer_profile,name="volunteer_profile"),
    path('dashboard/<int:vol_id>/', views.volunteer_dashboard, name="volunteer_dashboard"),

]