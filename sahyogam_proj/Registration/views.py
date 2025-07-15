from django.shortcuts import render, redirect, get_object_or_404
from .models import Volunteer, Organization
import re
import requests


    
def verify_pan_via_gst(pan):
    url = "https://commonapi.in/gst-pan-search"
    payload = {"pan": pan}
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",  # 🔁 Replace this with your actual key
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        print("🔍 PAN Lookup Response:", data)

        if data.get("success") and data.get("data"):
            # Optional: validate org name here
            return True
        else:
            return False
    except Exception as e:
        print("[ERROR] PAN verification failed:", e)
        return False
    
    
# --- Helpers ---
def detect_org_type(reg_no):
    if re.match(r'^[0-9]{6,7}$', reg_no):
        return "FCRA"
    elif re.match(r'^[LU][0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}$', reg_no):
        return "CIN"
    elif re.match(r'^[A-Z]/[0-9]{3,6}$', reg_no):
        return "NGO"
    elif re.match(r'^[A-Z]{2}/[0-9]{4}/[0-9]{7}$', reg_no):  # Darpan format
        return "DARPAN"
    else:
        return "Unknown"
    
    
    
    

# --- Main View ---
def registrations(request):
    error = None

    if request.method == "POST":
        user_type = request.POST.get("user_type")

        # --- Volunteer Registration ---
        if user_type == "Volunteer":
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

        # --- Organization Registration ---
        elif user_type == "Organization":
            reg_no = request.POST.get("reg_number")

            # ✅ Check registration number
            if not verify_pan_via_gst(reg_no):
                print("You entered Reg No:", reg_no)
                error = "❌ Invalid or unverified registration number."
                return render(request, "registrations.html", {"error": error})

            # ✅ Save organization if verified
            org = Organization.objects.create(
                org_name=request.POST.get("org_name"),
                org_reg_number=reg_no,
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

    return render(request, "registrations.html", {"error": None})


#  befor add check org by number 
# def registrations(request):
#     if request.method == "POST":
#         user_type = request.POST.get("user_type")

#         if user_type == "Volunteer":
#             # Collect Volunteer Data
#             volunteer = Volunteer.objects.create(
#                 volunteer_fname=request.POST.get("full_name"),
#                 volunteer_email=request.POST.get("email"),
#                 volunteer_phno=request.POST.get("phone"),
#                 volunteer_dob=request.POST.get("dob"),
#                 volunteer_city=request.POST.get("city"),
#                 volunteer_state=request.POST.get("state"),
#                 volunteer_pincode=request.POST.get("pincode"),
#                 volunteer_skill=((request.POST.get("skills") or "") + " " + (request.POST.get("skills1") or "")).strip(),
#                 volunteer_experience_years=int(request.POST.get("experience") or 0),
#                 volunteer_availability=request.POST.get("availability"),
#                 volunteer_consent_public=request.POST.get("agree_consent_public") == "on",
#                 volunteer_agree_to_terms=request.POST.get("agree_terms") == "on"
#             )
#             return redirect("volunteer_dashboard", vol_id=volunteer.id)

#         elif user_type == "Organization":
#             # Collect Organization Data
#             org = Organization.objects.create(
#                 org_name=request.POST.get("org_name"),
#                 org_reg_number=request.POST.get("reg_number"),
#                 org_type=request.POST.get("org_type"),
#                 org_established_yer=request.POST.get("established"),
#                 org_address=request.POST.get("address"),
#                 org_city=request.POST.get("city"),
#                 org_state=request.POST.get("state"),
#                 org_country=request.POST.get("country"),
#                 org_pincode=request.POST.get("pincode"),
#                 org_contact_person=request.POST.get("contact_person"),
#                 org_contact_email=request.POST.get("contact_email"),
#                 org_contact_phone=request.POST.get("contact_phone"),
#                 org_registered_doc=request.FILES.get("org_reg_doc"),
#                 org_agree_to_terms=request.POST.get("org_agree_to_terms") == "on"
#             )
#             return redirect("organization_profile", org_id=org.id)

#     return render(request, "registrations.html")

# def volunteer_profile(request, volunteer_id):
#     volunteer = get_object_or_404(Volunteer, id=volunteer_id)
#     return render(request, "volunteer_profile.html", {"volunteer": volunteer})

# def organization_profile(request, org_id):
#     org = get_object_or_404(Organization, id=org_id)
#     return render(request, "organization/organization_profile.html", {"org": org})

def about(request):
    return render(request,"about.html")



from django.shortcuts import render
import re

def pan_form(request):
    result = None
    pan = ""

    if request.method == "POST":
        pan = request.POST.get("pan", "").strip().upper()

        if re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan):
            result = f"✅ {pan} is a valid PAN format."
        else:
            result = f"❌ {pan} is NOT a valid PAN format."

    return render(request, "pan_check.html", {"result": result, "pan": pan})
