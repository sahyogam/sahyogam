
from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('', views.signup_login_view, name='signup_login'),        # Unified signup/login page 
    path('', views.register_view, name='register'),

    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    
    path('404/', views.page_404, name='404'),
    path('base/', views.base_page, name='base'),
    path('campaign-detail/', views.campaign_detail, name='campaign-detail'),
    path('certificates/', views.certificates, name='certificates'),
    path('explore/', views.explore, name='explore'),
    path('h1/', views.h1_page, name='h1'),
    path('h2/', views.h2_page, name='h2'),
    path('login/', views.login_page, name='login'),
    path('messages/', views.messages_page, name='messages'),
    path('post-campaign/', views.post_campaign, name='post-campaign'),
    path('signup-login/', views.signup_login, name='signup-login'),
    path('verify-otp/', views.verify_otp, name='verify-otp'),
    path('home/', views.home, name='home')
    
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
