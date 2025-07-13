from django.shortcuts import render
from Registration.models import Volunteer
# Create your views here.


def volunteer_profile(request,vol_id):
    volunteer = Volunteer.objects.get(id=vol_id)
    return render(request,"volunteer_profile.html",{"volunteer":volunteer})


def volunteer_dashboard(request, vol_id):
    volunteer = Volunteer.objects.get(id=vol_id)
    return render(request, "volunteer_dashboard.html", {"volunteer": volunteer})
