from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Organization, Volunteer, OTPVerification
import random


def register_view(request):
    return render(request, "register.html")


def verify_otp_view(request):
    return render(request, "otp.html")


def page_404(request):
    return render(request, '404.html')

def base_page(request):
    return render(request, 'base.html')

def campaign_detail(request):
    return render(request, 'campaign-detail.html')

def certificates(request):
    return render(request, 'certificates.html')

def explore(request):
    return render(request, 'explore.html')

def h1_page(request):
    return render(request, 'h1.html')

def h2_page(request):
    return render(request, 'h2.html')

def login_page(request):
    return render(request, 'login.html')

def messages_page(request):
    return render(request, 'messages.html')

def post_campaign(request):
    return render(request, 'post-campaign.html')

def signup_login(request):
    return render(request, 'signup_login.html')

def verify_otp(request):
    return render(request, 'verify_otp.html')

def home(request):
    return render(request, 'home.html')