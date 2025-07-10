from django.shortcuts import render
from django.http import HttpResponse
from .models import Volunteer,Organization

# Create your views here.
def registrations(request):
    if request.method == "POST":
        userType = request.POST.get("user_type")
        
        if userType == "Volunteer":
              
            volunteer_fname = request.POST.get("full_name")
            volunteer_email = request.POST.get("email")
            volunteer_phno = request.POST.get("phone")
            volunteer_dob = request.POST.get("dob")
            volunteer_city = request.POST.get("city")
            volunteer_state = request.POST.get("state")
            volunteer_pincode = request.POST.get("pincode")
        
            volunteer_skill=""
        
            if request.POST.get("skills") and request.POST.get("skills1"):
                volunteer_skill = request.POST.get("skills") +" "+ request.POST.get("skills1")
            elif request.POST.get("skills"):
                volunteer_skill = request.POST.get("skills")
            elif request.POST.get("skills1"):
                volunteer_skill = request.POST.get("skills1")            
            
            volunteer_experience_years = request.POST.get("experience")
            volunteer_availability = request.POST.get("availability")
            volunteer_consent_public = request.POST.get("agree_consent_public")
        
            if volunteer_consent_public == "on":
                volunteer_consent_public = True
            else:
                volunteer_consent_public = False            
        
            volunteer_agree_to_terms = request.POST.get("agree_terms")
        
            if volunteer_agree_to_terms == "on":
                volunteer_agree_to_terms = True
            else:
                volunteer_agree_to_terms = False
                
                
            volunteer = Volunteer.objects.create(volunteer_fname=volunteer_fname,volunteer_email=volunteer_email,volunteer_phno=volunteer_phno,volunteer_dob=volunteer_dob,volunteer_city=volunteer_city,volunteer_state=volunteer_state,volunteer_pincode=volunteer_pincode,volunteer_skill=volunteer_skill,volunteer_experience_years=volunteer_experience_years,volunteer_availability=volunteer_availability,volunteer_consent_public=volunteer_consent_public,volunteer_agree_to_terms=volunteer_agree_to_terms)
        
            context = {
                "volunteer_fname":volunteer_fname,
                "volunteer_email":volunteer_email,
                "volunteer_phno":volunteer_phno,
                "volunteer_dob":volunteer_dob,
                "volunteer_ct":volunteer_city,
                "volunteer_state":volunteer_state,
                "volunteer_pincode":volunteer_pincode,
                "volunteer_skill":volunteer_skill,
                "volunteer_experience_years":volunteer_experience_years,
                "volunteer_availability":volunteer_availability,
                "volunteer_consent_public":volunteer_consent_public,
                "volunteer_agree_to_terms":volunteer_agree_to_terms,
                "userType":userType
                }
        
            if volunteer:
                return render(request,"registrations.html",{"msg":True})
            
            return render(request,"registrations.html")
            
        else:
            org_name = request.POST.get("org_name")
            org_reg_number = request.POST.get("reg_number")
            org_type = request.POST.get("org_type")
            org_established_yer = request.POST.get("established")
            org_address = request.POST.get("address")
            org_city = request.POST.get("city")
            org_state = request.POST.get("state")
            org_country = request.POST.get("country")
            org_pincode = request.POST.get("pincode")
            org_contact_person = request.POST.get("contact_person")
            org_contact_email = request.POST.get("contact_email")
            org_contact_phone = request.POST.get("contact_phone")
            org_reg_doc= request.POST.get("org_reg_doc")
            
            org_agree_to_terms= request.POST.get("org_agree_to_terms")
            if request.POST.get("org_agree_to_terms") == "on":
                org_agree_to_terms = True
            else:
                org_agree_to_terms = False
            
            
            context = {
                "org_Name":org_name,
                "org_reg_number":org_reg_number,
                "org_type":org_type,
                "org_established_yer":org_established_yer,
                "org_address":org_address,
                "org_city":org_city,
                "org_state":org_state,
                "org_country":org_country,
                "org_contact_person":org_contact_person,
                "org_contact_email":org_contact_email,
                "org_contact_phone":org_contact_phone,  
                "org_reg_doc":org_reg_doc,
                "org_agree_to_terms":org_agree_to_terms                                
            }
            
            org_register = Organization.objects.create(org_name=org_name,org_reg_number=org_reg_number,org_type=org_type,org_established_yer=org_established_yer,org_address=org_address,org_city=org_city,org_state=org_state,org_country=org_country,org_contact_person=org_contact_person,org_contact_email=org_contact_email,org_contact_phone=org_contact_phone,org_registered_doc=org_reg_doc,org_agree_to_terms=org_agree_to_terms)
            
            if org_register:
                return render(request,"registrations.html",{"msg":True})

    return render(request,"registrations.html")
        
        
    

# def regisrationVolunteer(request):
    
    
def about(request):
    return render(request,"about.html")