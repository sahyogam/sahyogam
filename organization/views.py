from django.shortcuts import get_object_or_404, render
from Registration.models import Organization

def organization_profile(request, org_id):
    org = get_object_or_404(Organization, id=org_id)
    return render(request, "organization/organization_profile.html", {"org": org})
