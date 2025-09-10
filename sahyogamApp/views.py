from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import random

from datetime import datetime


from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
from .models import Organization, Volunteer,EmailOTP,Campaign
from .utils import send_otp_email
from django.contrib.auth.hashers import check_password

from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
import socket

def generate_otp():
    return str(random.randint(100000, 999999))


from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_otp_email(email, otp):
    
    subject = "Your Sahyogam Registration OTP"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [email]

    text_content = f"Your OTP is {otp}. It is valid for 3 minutes."  # plain text fallback

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; text-align: center; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            
            <!-- Logo -->
            <img src="https://lh3.googleusercontent.com/a-/ALV-UjXRqxHxsCB_ZfSeBy0DxjgZntFdrwjx3t_Igr2guK05gH5thZs=s100-p-k-rw-no" alt="Sahyogam Logo" style="
  
  
  --size: 140px;width: var(--size);
  height: var(--size);
  aspect-ratio: 1 / 1;     
  border-radius: 50%;      
  border: 1px solid #033761; 
  object-fit: cover;       
  display: inline-block;">
            
            <h2 style="color: #4CAF50;">Sahyogam OTP Verification</h2>
            <p style="font-size: 16px;">Your One-Time Password is:</p>
            <h1 style="color: #333; letter-spacing: 3px;">{otp}</h1>
            <p style="font-size: 14px; color: #555;">Valid for <strong>3 minutes</strong>. Please do not share it with anyone.</p>


            <p style="margin-top: 20px; font-size: 12px; color: gray;">This is an automated email from Sahyogam.</p>
        </div>
    </body>
    </html>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()




from django.shortcuts import render, redirect
from .models import Organization, Volunteer

def login_page(request):
    if request.method == "POST":
        role = request.POST.get("role")
        entered_email = request.POST.get("email","").strip()
        password = request.POST.get("password","").strip()

        if role == "organization":
            org = Organization.objects.filter(email__iexact=entered_email).first()
            
            
            if org and check_password(password,org.password):
                org = Organization.objects.get(email__iexact=entered_email)
                
                # request.session["OrgName"] = org.name
                # request.session["userType"] = "Organization"
                request.session["isOrgLogin"] = True
                request.session["org_dp"] = org.profile_photo.url if org.profile_photo else None

                request.session["org_name"] = org.name
                
                
                Campaigns =  Campaign.objects.all() 
                               
                context = {
                        "OrgName":org.name,
                        "ORG_DP":request.session["org_dp"],
                        "userType":"Organization",
                        "Campaigns":Campaigns,
                        "nav":True
                        }           
                
                # return render(request, 'organizationHome.html',context)
                return redirect("organizationHome")

            else:
                
             return render(request, 'login.html',{"ErrorMSG":True,"nav":False})


        elif role == "volunteer":
            vol = Volunteer.objects.filter(email__iexact=entered_email).first()
            
            request.session["VolPK"] = vol.pk
            
            if vol and check_password(password,vol.password):
                vol = Volunteer.objects.get(email__iexact=entered_email)
                
                
                request.session["isVolLogin"] = True
                request.session["vol_dp"] = vol.profile_photo.url if vol.profile_photo else None
                request.session["vol_email"] = vol.email
                return redirect("volunteerHome") 
                
                # context = {
                #     "VolName":vol.name,
                #     "userType":"Volunteer",
                #     "VOL_DP":request.session["vol_dp"],
                #     "pk":request.session["VolPK"],
                #     "skills":vol.skills.split(","), 
                #     "userName" : vol.username
                    
                # }
                
                # return render(request, 'volunteerHome.html',context)
                
            else:
             return render(request, 'login.html',{"ErrorMSG":True,"nav":False})


    return render(request, 'login.html',{"nav":False})


def register_volunteer(request):
      
    if request.method == "POST":
        
        # register_as = request.POST.get("register-as")
        
        request.session["register_as"] = "volunteer"
        
                                 
        name = request.POST.get("vol-name")
        username = request.POST.get("vol-username")
        email = request.POST.get("vol-email")
        phone = request.POST.get("vol-phone")
        password = request.POST.get("vol-password")
        confirm_password = request.POST.get("vol-confirm-password")
        skills = request.POST.get("skills", "")  
        location = request.POST.get("vol-location")
        profile_image = request.FILES.get("vol_profile_image_upload")
        
        # profile_image = request.FILES.get("vol_profile_image_upload")
            
        if profile_image:
            from django.core.files.storage import default_storage
            file_path = default_storage.save(f"images/{profile_image.name}", profile_image)

        request.session["vol_name"] = name
        request.session["vol_username"] = username
        request.session["vol_email"] = email
        request.session["vol_phone"] = phone
        request.session["vol_skills"] = skills
        request.session["vol_location"] = location
        request.session["vol_dp"] = file_path

        if password != confirm_password:
                
                return render(request, "register.html",{"ErrMSG":"Password and confirm password does not match !"})
            
        else:
                request.session["vol_password"] = password                         

        try:
                
                if Volunteer.objects.filter(email__iexact=email).exists():
                    
                    return render(request, "register.html",{"ErrMSG":"Email already registered !"})
                
             #generate and save OTP
                otp = generate_otp()
                EmailOTP.objects.filter(email=email).delete()
                EmailOTP.objects.create(email=email, otp=otp)
            
            #Send OTP
                send_otp_email(email, otp)
            
            
            # Store name and email in session for later
                request.session["temp_name"] = name
                request.session["temp_email"] = email
                
                return redirect("verify_otp")
            
        except (socket.gaierror, socket.timeout):
            # No internet or DNS resolution failed
                # messages.error(request, "Unable to send OTP. Please check your internet connection.")
                return render(request,"register.html",{"MailErrMSG":"Unable to send OTP. Please check your internet connection"})
                

        except BadHeaderError:
                # messages.error(request, "Invalid header found in email.")
                return render(request,"register.html",{"MailErrMSG":"Invalid header found in email"})
                

        except Exception as e:
            # Catch all other unexpected email errors
                # messages.error(request, f"Error sending email: {e}")
                return render(request,"register.html",{"MailErrMSG":f"Error sending email: {e}"})                                                            
    else:
        return render(request, "register.html")

    
def register_organization(request):
  
    if request.method == "POST":
    
    
        request.session["register_as"] = "organization"
        
        # if register_as == "organization":
        name = request.POST.get("org-name")
        email = request.POST.get("org-email")
        phone = request.POST.get("org-phone")
        password = request.POST.get("org-password")
        confirm_password = request.POST.get("org-confirm-password")
        org_type = request.POST.get("org-type")
        address = request.POST.get("org-address")    
            
        # profile_image = "../static/images/profile.png"
            
        # if profile_image:
        #     from django.core.files.storage import default_storage
        #     file_path = default_storage.save(f"images/{profile_image.name}", profile_image)
                
        request.session["org_dp"] = "../static/images/profile.png"  
            
        request.session["org_name"] = name
        request.session["org_email"] = email
        request.session["org_phone"] = phone
        request.session["org_confirm_password"] = confirm_password
        request.session["org_type"] = org_type
        request.session["org_address"] = address
            
            

        if password != confirm_password:
            return render(request, "register.html",{"ErrMSG":"Password and confirm password does not match !"})
        else:
            request.session["org_password"] = password
                
            
        try:
            if Organization.objects.filter(email__iexact=email).exists():
                return render(request, "register.html",{"ErrMSG":"Email already registered !"})
                
            #generate and save OTP
            otp = generate_otp()
            EmailOTP.objects.filter(email=email).delete()
            EmailOTP.objects.create(email=email, otp=otp)
            
            #Send OTP
            send_otp_email(email, otp)
                
                # Store name and email in session for later
            request.session["temp_name"] = name
            request.session["temp_email"] = email
            
            return redirect("verify_otp")
                
    
        except (socket.gaierror, socket.timeout):
            # No internet or DNS resolution failed
                # messages.error(request, "Unable to send OTP. Please check your internet connection.")
            return render(request,"register.html",{"ErrMSG":"Unable to send OTP. Please check your internet connection"})

        except BadHeaderError:
                # messages.error(request, "Invalid header found in email.")
            return render(request,"register.html",{"ErrMSG":"Invalid header found in email"})
                

        except Exception as e:
            # Catch all other unexpected email errors
                # messages.error(request, f"Error sending email: {e}")   
            return render(request,"register.html",{"ErrMSG":f"Error sending email: {e}"})                    

    else:
        return render(request, "register.html")

def register(request):
    return render(request, "register.html")


def verify_otp_view(request):
    # if request.session["isLogin"] == False:
        
        email = request.session["temp_email"]
        
        if not email:
            return redirect("register")
    
        if request.method == "POST":
            entered_otp = request.POST.get("otp")
            try:
                    otp_obj = EmailOTP.objects.get(email=email)
                    
            except EmailOTP.DoesNotExist:
                    # messages.error(request, "OTP not found. Please resend.")
                    # return redirect("verify_otp")
                    return render(request, "otp.html",{"ErrMsg":"OTP not found. Please resend"})


            if otp_obj.is_expired():
                    # messages.error(request, "OTP expired. Please resend.")
                    # return redirect("verify_otp")
                    return render(request, "otp.html",{"ErrMsg":"OTP expired. Please resend."})


            if entered_otp == otp_obj.otp:
                if request.session["register_as"] == "organization":
                                                
                    org_email = request.session["org_email"]
                    
                    Organization.objects.create(
                    name=request.session["org_name"],
                    email= org_email.upper(),
                    phone=request.session["org_phone"],
                    password=make_password(request.session["org_password"]),
                    org_type=request.session["org_type"],
                    address=request.session["org_address"],
                    profile_photo=request.session["org_dp"]                    
                    )   
                    
                    request.session["isOrgLogin"] = True
                    
                    del request.session["temp_name"]
                    del request.session["temp_email"]
                
                    # del request.session["org_name"]
                    # del request.session["org_email"]
                    del request.session["org_phone"]
                    del request.session["org_password"]
                    del request.session["org_type"]
                    del request.session["org_address"]
                    
                    otp_obj.delete()
                
                #go to dashboard
                #write here return code
                    return redirect("organizationHome")
                
                else:
                    
                    vol_email = request.session["vol_email"]
                
                    Volunteer.objects.create(
                    name=request.session["vol_name"],
                    username=request.session["vol_username"],
                    email=vol_email.upper(),
                    phone=request.session["vol_phone"],
                    password=make_password(request.session["vol_password"]),
                    skills=request.session["vol_skills"],
                    location=request.session["vol_location"],
                    profile_photo=request.session["vol_dp"]
                )
                
                    request.session["isVolLogin"] = True

                    del request.session["temp_name"]
                    # del request.session["temp_email"]
                    # del request.session["vol_name"]
                    del request.session["vol_username"]
                    # del request.session["vol_email"]
                    del request.session["vol_phone"]
                    del request.session["vol_password"]
                    del request.session["vol_skills"]
                    del request.session["vol_location"]
                    # del request.session["vol_dp"]
                
                    otp_obj.delete()
                    #return on volunteer dashboard
                    # 23-08-2025
                    # vol = get_object_or_404(Volunteer, email = request.session["vol_email"])
                    return redirect("volunteerHome")
            else:
                return render(request, "otp.html",{"email":request.session["temp_email"],"ErrMsg":"Invalid OTP!"})

        else:
            return render(request, "otp.html",{"email":request.session["temp_email"]})

        
    
def resend_otp_view(request):
    # if request.session["isLogin"] == False:
    email = request.session.get("temp_email")
    if not email:
        return redirect("register")

    otp = generate_otp()
    
    EmailOTP.objects.filter(email=email).delete()
    EmailOTP.objects.create(email=email, otp=otp)
    send_otp_email(email, otp)
    messages.success(request, "A new OTP has been sent to your email.")
    return redirect("verify_otp")




def page_404(request):
    return render(request, '404.html')

def base_page(request):
    return render(request, 'base.html')

def campaign_detail(request):
    return render(request, 'campaign-detail.html',{"nav":True})

def certificates(request):
    return render(request, 'certificates.html')

def explore(request):
    return render(request, 'explore.html',{"nav":True,"search":True})

def volunteerHome(request):
    try:
        if request.session["isVolLogin"] == True:
            
                Campaigns =  Campaign.objects.all()           
                vol = Volunteer.objects.get(email__iexact=request.session["vol_email"])                          
                
                request.session["vol_dp"] = vol.profile_photo.url if vol.profile_photo else None
                
                context = {
                    "VolName":vol.name,
                    "VOL_DP":request.session["vol_dp"],
                    "userType":"Volunteer",
                    "skills":vol.skills.split(","),
                    "pk":vol.pk,
                    "userName" : vol.username,
                    "Campaigns":Campaigns,
                    "nav":True,
                    "search":False,
                    "logoutLink":True
                    
                }
            
                return render(request, 'volunteerHome.html',context)
        else:
            return redirect("register")
    except Exception as e:
            # Catch all other unexpected email errors
                # messages.error(request, f"Error sending email: {e}")
            return redirect("login")


def organizationHome(request):
    if request.session["isOrgLogin"] == True:
        
        Campaigns =  Campaign.objects.all()                
        
        # org = Organization.objects.all()  
        
        
        context = {
            "OrgName":request.session["org_name"],
            "ORG_DP":request.session["org_dp"],
            "userType":"Organization",
            "Campaigns":Campaigns,
            # "nav":True
            
        }
        return render(request, 'organizationHome.html',context)
    else:
        return redirect("login")


def messages_page(request):
    return render(request, 'messages.html')

def post_campaign(request,OrgName):
    
    if request.method == "POST":
        campaignTitle = request.POST.get("campaignTitle")
        shortDescription = request.POST.get("shortDescription")
        fullDescription = request.POST.get("fullDescription")
        skills = request.POST.get("skills")
                
        
        location = request.POST.get("location")
        totalVolunteers = request.POST.get("totalVolunteers")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")
        timeSlot = request.POST.get("timeSlot")
        additionalInstructions = request.POST.get("additionalInstructions")
                
        bannerImage = request.FILES.get("bannerImage")
        if bannerImage:
            from django.core.files.storage import default_storage
            file_path = default_storage.save(f"images/{bannerImage.name}", bannerImage)
        
        
        Campaign.objects.create(
            title=campaignTitle,
            short_description=shortDescription,
            full_description=fullDescription,
            skills_required=skills,
            location=location,
            total_volunteers_needed=totalVolunteers,
            applied = 0,
            start_date=startDate,
            end_date=endDate,
            time_slot=timeSlot,
            banner_image=file_path,
            additional_instructions=additionalInstructions,
            postedBy = OrgName
        )
        
        
        context = {
           "CampMsg":"Campaign Posted Successfuly"
        }
        
        return render(request,'post-campaign.html',context)
        
    
    return render(request, 'post-campaign.html')
    

    

def verify_otp(request):
    return render(request, 'verify_otp.html')

def home(request):
    return render(request, 'home.html')



def logout(request,userID):
    if userID == 'org' :
        del request.session["isOrgLogin"]
        return redirect("login")
        
    if userID == 'vol' :
        del request.session["isVolLogin"]
        return redirect("login") 
                
    # return redirect("login")
    
def edit_volunteer(request, pk):
    volunteer = get_object_or_404(Volunteer, pk=pk)

    if request.method == "POST":
        volunteer.name = request.POST.get("name")
        volunteer.username = request.POST.get("username")
        volunteer.phone = request.POST.get("phone")
        

        if request.POST.get("skills") == "":
            volunteer.skills = volunteer.skills
        else:
            volunteer.skills = request.POST.get("skills")

        volunteer.location = request.POST.get("location")
        
        profile_image = request.FILES.get("profile_photo")
            
        if profile_image:
            from django.core.files.storage import default_storage
            file_path = default_storage.save(f"images/{profile_image.name}", profile_image)

            volunteer.profile_photo = file_path            


        volunteer.save()
        # 23-08-2025 setup PK for uniqueness of each user and updation code remain
        return redirect("volunteerHome")

    return render(request, "edit_volunteer.html", {"volunteer": volunteer})


def detailCampaign(request,pk,userType):
    campaignData = Campaign.objects.get(pk=pk)
        
    applyBtn = True
        
    if userType == "Organization":
        applyBtn = False                
    
    context = {
        "pk":campaignData.pk,
        "title": campaignData.title,
        "short_description":campaignData.short_description,
        "full_description":campaignData.full_description,
        "skills_required":campaignData.skills_required,
        "location":campaignData.location,
        "total_volunteers_needed":campaignData.total_volunteers_needed,
        "applied":campaignData.applied,
        "start_date":campaignData.start_date,
        "end_date":campaignData.end_date,
        "time_slot":campaignData.time_slot,
        "banner_image":campaignData.banner_image.url if campaignData.banner_image else None ,
        "additional_instructions":campaignData.additional_instructions,
        "created_at":campaignData.created_at,
        "updated_at":campaignData.updated_at,
        "applyBtn":applyBtn,             
        "userType":userType,
        "nav":True,
        "logoutLink":True
        
    }
    
    return render(request,"detailCampaign.html",context)


def deleteCampaign(request,pk):
    campaign = Campaign.objects.get(pk=pk)
    campaign.delete()
    
    return redirect("organizationHome")
    
