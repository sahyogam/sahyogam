

from django.shortcuts import render, redirect, get_object_or_404
from .models import Volunteer, Organization

def registrations(request):
    if request.method == "POST":
        user_type = request.POST.get("user_type")

        if user_type == "Volunteer":
            # Collect Volunteer Data
            volunteer = Volunteer.objects.create(
                volunteer_fname=request.POST.get("full_name"),
                volunteer_email=request.POST.get("email"),
                volunteer_phno=request.POST.get("phone"),
                volunteer_dob=request.POST.get("dob"),
                volunteer_city=request.POST.get("city"),
                volunteer_state=request.POST.get("state"),
                volunteer_pincode=request.POST.get("pincode"),
                volunteer_skill=((request.POST.get("skills") or "") + " " + (request.POST.get("skills1") or "")).strip(),
                volunteer_experience_years=int(request.POST.get("experience") or 0),
                volunteer_availability=request.POST.get("availability"),
                volunteer_consent_public=request.POST.get("agree_consent_public") == "on",
                volunteer_agree_to_terms=request.POST.get("agree_terms") == "on"
            )
            return redirect("volunteer_dashboard", vol_id=volunteer.id)

        elif user_type == "Organization":
            # Collect Organization Data
            org = Organization.objects.create(
                org_name=request.POST.get("org_name"),
                org_reg_number=request.POST.get("reg_number"),
                org_type=request.POST.get("org_type"),
                org_established_yer=request.POST.get("established"),
                org_address=request.POST.get("address"),
                org_city=request.POST.get("city"),
                org_state=request.POST.get("state"),
                org_country=request.POST.get("country"),
                org_pincode=request.POST.get("pincode"),
                org_contact_person=request.POST.get("contact_person"),
                org_contact_email=request.POST.get("contact_email"),
                org_contact_phone=request.POST.get("contact_phone"),
                org_registered_doc=request.FILES.get("org_reg_doc"),
                org_agree_to_terms=request.POST.get("org_agree_to_terms") == "on"
            )
            return redirect("organization_profile", org_id=org.id)

    return render(request, "registrations.html")

# def volunteer_profile(request, volunteer_id):
#     volunteer = get_object_or_404(Volunteer, id=volunteer_id)
#     return render(request, "volunteer_profile.html", {"volunteer": volunteer})

# def organization_profile(request, org_id):
#     org = get_object_or_404(Organization, id=org_id)
#     return render(request, "organization/organization_profile.html", {"org": org})

def about(request):
    return render(request,"about.html")