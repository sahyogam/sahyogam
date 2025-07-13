from django.shortcuts import render, get_object_or_404, redirect
from Registration.models import Organization, Volunteer
from .models import OrganizationProfile, VolunteerProfile
from .forms import OrganizationProfileForm, VolunteerProfileForm

def organization_profile_page(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    profile, _ = OrganizationProfile.objects.get_or_create(organization=organization)

    if request.method == 'POST':
        form = OrganizationProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = OrganizationProfileForm(instance=profile)

    return render(request, 'profile_page/organization_profile.html', {
        'organization': organization,
        'form': form,
    })

def delete_org_photo(request, org_id):
    profile = get_object_or_404(OrganizationProfile, organization__id=org_id)

    if profile.profile_photo:
        profile.profile_photo.delete(save=False)
        profile.profile_photo = None
        profile.save()

    return redirect('organization_profile_page', org_id=org_id)

def volunteer_profile_page(request, vol_id):
    volunteer = get_object_or_404(Volunteer, id=vol_id)
    profile, _ = VolunteerProfile.objects.get_or_create(volunteer=volunteer)

    if request.method == 'POST':
        form = VolunteerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = VolunteerProfileForm(instance=profile)

    return render(request, 'profile_page/volunteer_profile.html', {
        'volunteer': volunteer,
        'form': form,
    })

def delete_vol_photo(request, vol_id):
    profile = get_object_or_404(VolunteerProfile, volunteer__id=vol_id)

    if profile.profile_photo:
        profile.profile_photo.delete(save=False)
        profile.profile_photo = None
        profile.save()

    return redirect('volunteer_profile_page', vol_id=vol_id)
