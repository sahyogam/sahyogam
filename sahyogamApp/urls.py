
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
    
    path('delete-campaign/<int:pk>', views.deleteCampaign, name='delete-campaign'),

    path("edit-campaign/<str:userType>/<int:pk>/",views.editCampaign,name="EditCampaign"),
        
    path('edit-organization/<int:PK>/',views.editOrganization,name="editOrganization"),
    
    path('detailCampaign/<int:pk>/<str:userType>/<int:Upk>/',views.detailCampaign,name="detailCampaign"),
    
    # path('404/', views.page_404, name='404'),
    path('base/', views.base_page, name='base'),
    path('campaign-detail/', views.campaign_detail, name='campaign-detail'),
    path('explore/', views.explore, name='explore'),
    path("request_for_campaing/<int:OrgPk>/<int:VolPk>/",views.request_for_campaing,name="request_for_campaing"),
    path("invitationsList/<int:VolPk>/",views.invitationsList,name="invitationsList"),
    path("cancel_invite/<int:pk>/<int:VolPk>/",views.cancel_invite,name="cancel_invite") ,
    path("exploreOrg/",views.exploreOrg,name="exploreOrg"),
    path('volunteerHome/', views.volunteerHome, name='volunteerHome'),
    path('organizationHome/', views.organizationHome, name='organizationHome'),
    path('login/', views.login_page, name='login'),
    path('messages/', views.messages_page, name='messages'),
    
    path('home/', views.home, name='home'), 

    path("logout/<str:userID>/",views.logout,name="logout"),
    
    path('totalVolunteerApplied/', views.totalVolunteerApplied, name='totalVolunteerApplied'),
    
    path(
        'certificate_pdf/<int:volunteer_id>/<int:campaign_id>/',
        views.certificate_pdf,
        name='download_certificate'
    ),
    
    path(
        'invited_certificate_pdf/<int:volunteer_id>/<int:invited_campaign_id>/',
        views.invited_certificate_pdf,
        name='download_invited_certificate'
    ),


    path("totalInvitationsGot/<int:OrgPk>/",views.totalInvitationsGot,name="totalInvitationsGot"),
    
    
    path("certificates/<int:volunteer_id>/", views.volunteer_certificates, name="volunteer_certificates"),
    path("approve_certificate/<str:type>/<int:campaign_id>/<int:volunteer_id>/", views.approve_certificate, name="approve_certificate"),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.conf.urls import handler404
handler404 = views.page_404
