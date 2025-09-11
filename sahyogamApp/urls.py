
from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', views.login_page, name='login'),
    
    path('register/', views.register, name='register'),
    
    path("register_organization/",views.register_organization,name="register_organization"),
    path("register_volunteer/",views.register_volunteer,name="register_volunteer"),  
    path("edit_volunteer/<int:pk>/",views.edit_volunteer,name="edit_volunteer"),
    
    # path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),
    path('post-campaign/<str:OrgName>', views.post_campaign, name='post-campaign'),
    
    path("edit-capaign/<int:pk>",views.editCampaign,name="editCampaing"),
    path('delete-campaign/<int:pk>', views.deleteCampaign, name='delete-campaign'),
    
    path('edit-organization',views.editOrganization,name="editOrganization"),
    
    path('detailCampaign/<int:pk>/<str:userType>/',views.detailCampaign,name="detailCampaign"),
    
    # path('404/', views.page_404, name='404'),
    path('base/', views.base_page, name='base'),
    path('campaign-detail/', views.campaign_detail, name='campaign-detail'),
    path('certificates/', views.certificates, name='certificates'),
    path('explore/', views.explore, name='explore'),
    path('volunteerHome/', views.volunteerHome, name='volunteerHome'),
    path('organizationHome/', views.organizationHome, name='organizationHome'),
    path('login/', views.login_page, name='login'),
    path('messages/', views.messages_page, name='messages'),
    path('home/', views.home, name='home'), 

    path("logout/<str:userID>/",views.logout,name="logout"),
    
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.conf.urls import handler404
handler404 = views.page_404
