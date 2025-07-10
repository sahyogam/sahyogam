from django.urls import path
from . import views
urlpatterns = [
    path("",views.registrations,name="registration"),
    path("about/",views.about,name="about")
]