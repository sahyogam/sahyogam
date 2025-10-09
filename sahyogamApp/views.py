from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from .models import AppliedCampaign  
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet
from .models import Organization, AppliedCampaign
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import random
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
from .models import Organization, Volunteer,EmailOTP,Campaign,AppliedCampaign
from .utils import send_otp_email
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
import socket
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Frame


def generate_otp():
    return str(random.randint(100000, 999999))
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
                
                
                request.session["isOrgLogin"] = True
                request.session["org_dp"] = org.profile_photo.url if org.profile_photo else None

                request.session["org_name"] = org.name
                
                request.session["org_email"] = entered_email
                
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
                
                
            else:
             return render(request, 'login.html',{"ErrorMSG":True,"nav":False})


    return render(request, 'login.html',{"nav":False})


def register_volunteer(request):
      
    if request.method == "POST":
        
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

def page_404(request, exception):
    return render(request, "404.html", status=404)

def base_page(request):
    return render(request, 'base.html')

def campaign_detail(request):
    return render(request, 'campaign-detail.html',{"nav":True})

def certificates(request):
    return render(request, 'certificates.html')

def explore(request):
    campaign =  Campaign.objects.all()
    vol = Volunteer.objects.get(email__iexact=request.session["vol_email"])                          
    
    context = {
        "nav":True,
        "search":True,
        "Campaigns":campaign,
        "logoutLink":True,
        "pk":vol.pk,
        "VolName":vol.name,
        "VOL_DP":request.session["vol_dp"],
        "userType":"Volunteer",
        "skills":vol.skills.split(","),
        "pk":vol.pk,
        "userName" : vol.username,
        # "Campaigns":Campaigns,
        "nav":True,
        "search":False,
        "logoutLink":True,
        # "explore_button":True
        
        
    }
    
    return render(request, 'explore.html',context)

def volunteerHome(request):
    try:
        if request.session["isVolLogin"] == True:
            
                vol = Volunteer.objects.get(email__iexact=request.session["vol_email"])

                applied_entries = AppliedCampaign.objects.select_related('volunteer','campaign').filter(volunteer_id=vol.pk)
                
                request.session["vol_dp"] = vol.profile_photo.url if vol.profile_photo else None
                
                context = {
                    "VolName":vol.name,
                    "VOL_DP":request.session["vol_dp"],
                    "userType":"Volunteer",
                    "skills":vol.skills.split(","),
                    "pk":vol.pk,
                    "userName" : vol.username,
                    "Campaigns":applied_entries,
                    "nav":True,
                    "search":False,
                    "logoutLink":True,
                    "explore_button":True,
                    # "entries":applied_entries
                    
                }
            
                return render(request, 'volunteerHome.html',context)
        else:
            return redirect("register")
    except Exception as e:
        
            # Catch all other unexpected email errors
                # messages.error(request, f"Error sending email: {e}")
        print(e)
        return redirect("login")


def organizationHome(request):
    try:
        if request.session["isOrgLogin"] == True:
        
            org = Organization.objects.get(email__iexact=request.session["org_email"])  
            # vol = Volunteer.objects.get(email__iexact=request.session["vol_email"])                          
            
            campaign =  Campaign.objects.filter(organizationID=org)
            
            context = {
            "OrgName":org.name,
            "ORG_DP":request.session["org_dp"],
            "userType":"Organization",
            "Campaigns":campaign,
            # "nav":True,
            "PK":org.pk,
            "ORG":org
            
            
            }
            return render(request, 'organizationHome.html',context)
            
        else:
            return redirect("login")
    except Exception as e:
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
        
        start_time_str = request.POST.get("start_time")
        end_time_str = request.POST.get("end_time")
        
        
        if start_time_str:
            time_12 = datetime.strptime(start_time_str, "%H:%M").strftime("%I:%M %p")  
        else:
            time_12 = None

        starting_time = time_12
        
        if end_time_str:
            time_12 = datetime.strptime(end_time_str, "%H:%M").strftime("%I:%M %p")  
        else:
            time_12 = None

        ending_time = time_12
        
        additionalInstructions = request.POST.get("additionalInstructions")
                
        bannerImage = request.FILES.get("bannerImage")
        if bannerImage:
            from django.core.files.storage import default_storage
            file_path = default_storage.save(f"images/{bannerImage.name}", bannerImage)
        
        org = Organization.objects.get(email__iexact=request.session["org_email"])  

        
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
            start_time=starting_time,
            end_time = ending_time,
            banner_image=file_path,
            additional_instructions=additionalInstructions,
            postedBy = OrgName,
            organizationID = org
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
        return redirect("explore")

    return render(request, "edit_volunteer.html", {"volunteer": volunteer})


def detailCampaign(request, pk, userType, Upk):
    campaignData = get_object_or_404(Campaign, pk=pk)

    if request.method == "POST" and userType != "Organization":
        volunteerData = get_object_or_404(Volunteer, pk=Upk)

        # check if already applied to this campaign
        if AppliedCampaign.objects.filter(volunteer=volunteerData, campaign=campaignData).exists():
            messages.warning(request, "You've already applied!")
            return redirect("volunteerHome")

        # get all campaigns volunteer has applied to
        applied_entries = AppliedCampaign.objects.select_related('campaign').filter(volunteer=volunteerData)

        new_start = campaignData.start_date
        new_end = campaignData.end_date

        # convert time strings (e.g. "10:00 AM") to time objects
        def parse_time(time_str):
            try:
                return datetime.strptime(time_str.strip(), "%I:%M %p").time() if time_str else None
            except Exception:
                return None

        new_start_time = parse_time(getattr(campaignData, "start_time", None))
        new_end_time = parse_time(getattr(campaignData, "end_time", None))

        # flag for overlap
        overlap_found = False

        for applied in applied_entries:
            old_campaign = applied.campaign
            old_start = old_campaign.start_date
            old_end = old_campaign.end_date
            old_start_time = parse_time(getattr(old_campaign, "start_time", None))
            old_end_time = parse_time(getattr(old_campaign, "end_time", None))

            # Check if date ranges overlap
            dates_overlap = not (new_end < old_start or new_start > old_end)

            # Check if time ranges overlap
            times_overlap = False
            if new_start_time and new_end_time and old_start_time and old_end_time:
                times_overlap = not (new_end_time <= old_start_time or new_start_time >= old_end_time)

            # If both overlap, block
            if dates_overlap and times_overlap:
                overlap_found = True
                messages.warning(
                    request,
                    f"You've already applied in another campaign ({old_campaign.title}) "
                    f"between {old_start}–{old_end} at similar time slot."
                )
                break

        if overlap_found:
            return redirect("volunteerHome")

        # Otherwise, apply new campaign
        AppliedCampaign.objects.create(
            volunteer=volunteerData,
            campaign=campaignData,
            applied_at=datetime.now().strftime("%I:%M %p"),
        )
        campaignData.applied += 1
        campaignData.save()
        messages.success(request, "You have successfully applied for this campaign.")
        return redirect("volunteerHome")

    # if GET request
    applyBtn = userType != "Organization"

    context = {
        "pk": campaignData.pk,
        "volPk": Upk,
        "title": campaignData.title,
        "short_description": campaignData.short_description,
        "full_description": campaignData.full_description,
        "skills_required": campaignData.skills_required,
        "location": campaignData.location,
        "total_volunteers_needed": campaignData.total_volunteers_needed,
        "applied": campaignData.applied,
        "start_date": campaignData.start_date,
        "end_date": campaignData.end_date,
        "start_time": campaignData.start_time,
        "end_time": campaignData.end_time,
        "banner_image": campaignData.banner_image.url if campaignData.banner_image else None,
        "additional_instructions": campaignData.additional_instructions,
        "applyBtn": applyBtn,
        "userType": userType,
        "nav": True,
        "logoutLink": True,
        "postedBy": campaignData.postedBy,
    }

    return render(request, "detailCampaign.html", context)

def deleteCampaign(request,pk):
    
    campaign = Campaign.objects.get(pk=pk)
    campaign.delete()
    
    return redirect("organizationHome")
    

def editCampaign(request,userType,pk):
    
    campaign = Campaign.objects.get(pk=pk)
    
    if request.method == "POST":
        campaignTitle = request.POST.get("campaignTitle")
        shortDescription = request.POST.get("shortDescription")
        fullDescription = request.POST.get("fullDescription")
        skills = request.POST.get("skills")
                
        
        location = request.POST.get("location")
        totalVolunteers = request.POST.get("totalVolunteers")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")
        additionalInstructions = request.POST.get("additionalInstructions")
                
        bannerImage = request.FILES.get("profile_photo")
        
        if bannerImage:
            from django.core.files.storage import default_storage
            file_path = default_storage.save(f"images/{bannerImage.name}", bannerImage)
            campaign.banner_image = file_path
        
        campaign.title = campaignTitle
        campaign.short_description = shortDescription
        campaign.full_description = fullDescription
        campaign.skills_required = skills
        campaign.location = location
        campaign.total_volunteers_needed = totalVolunteers
        campaign.applied = 0
        campaign.start_date = startDate
        campaign.end_date = endDate
        
        start_time_str = request.POST.get("start_time")
        
        # Starting time
        if start_time_str:
            time_12 = datetime.strptime(start_time_str, "%H:%M").strftime("%I:%M %p")  
        else:
            time_12 = None

        starting_time = time_12
        campaign.start_time = starting_time
        
        # Ending time
        end_time_str = request.POST.get("end_time")
        if end_time_str:
            time_12 = datetime.strptime(end_time_str, "%H:%M").strftime("%I:%M %p")  
        else:
            time_12 = None

        ending_time = time_12
        campaign.end_time = ending_time

        
        campaign.additional_instructions = additionalInstructions
        campaign.save()
        
        AppliedCampaign.objects.filter(campaign_id=pk).delete()

    
        # path('detailCampaign/<int:pk>/<str:userType>/<int:Upk>/',views.detailCampaign,name="detailCampaign"),
        
        context = {
              
        "pk":pk,
        "volPk":0,
        "title": campaignTitle,
        "short_description":shortDescription,
        "full_description":fullDescription,
        "skills_required":skills,
        "location":location,
        "total_volunteers_needed":totalVolunteers,
        "applied":0,
        "start_date":startDate,
        "end_date":endDate,
        "start_time":starting_time,
        "end_time":ending_time,
        "banner_image":campaign.banner_image.url if campaign.banner_image else None ,
        "additional_instructions":additionalInstructions,
        "created_at":campaign.created_at,
        "updated_at":campaign.updated_at,
        "applyBtn":False,             
        "userType":userType,
        "nav":True,
        "logoutLink":True,
        "postedBy":campaign.postedBy
        }
        
        
        return render(request,"detailCampaign.html",context)

    
    
    time_str = campaign.end_time  # e.g., "10:00 AM"
    try:
        formatted_end_time = datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")
    except ValueError:
        formatted_end_time = ""
    
    time_str = campaign.start_time  # e.g., "10:00 AM"
    try:
        formatted_start_time = datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")
    except ValueError:
        formatted_start_time = ""
    
    
    context = {
        "nav":True,
        "userType":userType,
        "campaign": campaign,
        "start_time":formatted_start_time,
        "end_time":formatted_end_time
        
        }


    return render(request,"edit_campaign.html",context)

def editOrganization(request,PK):
    
    org = get_object_or_404(Organization, pk=PK)
    
    if request.method == "POST":
        org.name = request.POST.get("name")
        org.username = request.POST.get("username")
        org.org_type = request.POST.get("org-type")
        org.phone = request.POST.get("phone")
        
        
        org.address = request.POST.get("address")
        
        profile_image = request.FILES.get("profile_photo")
            
        if profile_image:
            from django.core.files.storage import default_storage
            file_path = default_storage.save(f"images/{profile_image.name}", profile_image)

            org.profile_photo = file_path            


        org.save()
        return redirect("organizationHome")
    
    # campaign =  Campaign.objects.filter(organizationID=org)
    
    context = {
            # "OrgName":org.name,
            "ORG_DP":request.session["org_dp"],
            "userType":"Organization",
            # "Campaigns":campaign,
            "nav":False,
            "OrgData":org
            }
    return render(request,"edit_organization.html",context)


def logout(request,userID):
    
    if userID == 'org' :
        del request.session["isOrgLogin"]
        del request.session["org_dp"]
        del request.session["org_name"]
        
        return redirect("login")
        
    if userID == 'vol' :
        del request.session["isVolLogin"]
        del request.session["VolPK"]
        del request.session["vol_dp"]
        del request.session["vol_email"]
        
        return redirect("login") 
 


def totalVolunteerApplied(request):
    
    if request.method == "POST":
        CampaignPk = request.POST.get("CampaignPk")
        VolunteerPk = request.POST.get("VolunteerPk")
        status = request.POST.get("status")
        approveCerti = request.POST.get("approveCerti")

        applied_entry = AppliedCampaign.objects.select_related('volunteer', 'campaign').get(
            volunteer_id=VolunteerPk,
            campaign_id=CampaignPk,
        )

        applied_entry.status = status
        applied_entry.certificate_approved = approveCerti
        applied_entry.save()

        volunteer = applied_entry.volunteer
        campaign = applied_entry.campaign
        org = campaign.organizationID

        subject = f"Update on your Application for '{campaign.title}'"
        message = f"""
        
        Dear {volunteer.name},

        We wanted to update you about your application for the campaign: "{campaign.title}".

        🗓️ Campaign Duration: {campaign.start_date} to {campaign.end_date}
        ⏰ Time Slot: {campaign.start_time} - {campaign.end_time}

        Your current application status is: **{status.upper()}**
        """

        # Approve For Certificate? is YES then certificate generate:
        pdf_buffer = None
        if approveCerti == "True" and status.lower() == "accepted":
            message += "\n✅ Congratulations! You have been approved for a certificate. The certificate is attached to this email."

            # Generate certificate in-memory (BytesIO)
            pdf_buffer = BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=A4)
            width, height = A4

            # Border
            c.setStrokeColor(HexColor("#0D47A1"))
            c.setLineWidth(4)
            c.rect(30, 30, width - 60, height - 60)

            # Title
            c.setFont("Helvetica-Bold", 28)
            c.setFillColor(HexColor("#0D47A1"))
            c.drawCentredString(width / 2, height - 120, "CERTIFICATE")

            # Body
            c.setFont("Helvetica", 14)
            c.setFillColor(HexColor("#000000"))

            text = (
                f"This is to certify that {volunteer.name}, "
                f"for donating their valuable skill(s): {volunteer.skills}, "
                f"has successfully participated in the campaign "
                f"\"{campaign.title}\" organized by {org.name}."
            )

            styles = getSampleStyleSheet()
            style = styles["Normal"]
            style.fontSize = 14
            style.leading = 20

            p = Paragraph(text, style)
            frame = Frame(80, height / 2 - 60, width - 160, 120, showBoundary=0)
            frame.addFromList([p], c)

            # Footer
            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(width / 2, 120, f"With warm regards,")
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(width / 2, 90, org.name)

            c.showPage()
            c.save()
            pdf_buffer.seek(0)

        elif status.lower() == "rejected":
            message += "\nWe appreciate your interest, but unfortunately, you were not selected for this campaign."

        else:
            message += "\nYour application is currently pending review."

        message += f"\n\nBest regards,\n{org.name} Team"

        try:
            # Prepare email
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[volunteer.email],
            )

            # Attach certificate if available
            if pdf_buffer:
                email.attach(f"certificate_{volunteer.name}.pdf", pdf_buffer.getvalue(), "application/pdf")

            email.send()
            messages.success(request, f"Email sent to {volunteer.name} ({status}) successfully.")

        except Exception as e:
            messages.error(request, f"Status updated, but failed to send email: {e}")

    # Show all applied volunteers
    org = Organization.objects.get(email__iexact=request.session["org_email"])
    applied_entries = AppliedCampaign.objects.select_related('volunteer', 'campaign').filter(
        campaign__organizationID_id=org.pk
    )

    context = {"applied_entries": applied_entries}
    return render(request, "totalVolunteerApplied.html", context)



def certificate_pdf(request, volunteer_id, campaign_id):

    applied = AppliedCampaign.objects.select_related("volunteer", "campaign__organizationID").get(
        volunteer_id=volunteer_id,
        campaign_id=campaign_id,
        certificate_approved=True   
    )

    volunteer = applied.volunteer
    campaign = applied.campaign
    organization = campaign.organizationID

    # Prepare response
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="certificate_{volunteer.name}.pdf"'

    # Set up canvas
    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Background / border (optional)
    c.setStrokeColor(HexColor("#0D47A1"))
    c.setLineWidth(4)
    c.rect(30, 30, width - 60, height - 60)

    # Title
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(HexColor("#0D47A1"))
    c.drawCentredString(width / 2, height - 120, "CERTIFICATE")

    # Body text
    c.setFont("Helvetica", 14)
    c.setFillColor(HexColor("#000000"))

    text = (
        f"This is to certify that {volunteer.name}, "
        f"for donating their valuable skill(s): {volunteer.skills}, "
        f"has successfully participated in the campaign "
        f"\"{campaign.title}\" organized by {organization.name}."
    )

    # Wrap long text

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 14
    style.leading = 20

    p = Paragraph(text, style)
    frame = Frame(80, height/2 - 60, width - 160, 120, showBoundary=0)
    frame.addFromList([p], c)

    # Footer / greetings
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, 120, f"With warm regards,")
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, 90, organization.name)

    c.showPage()
    c.save()
    return response
