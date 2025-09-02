# from django import forms

# ROLE_CHOICES = [
#     ('organization', 'Organization'),
#     ('volunteer', 'Volunteer'),
# ]

# ORG_TYPE_CHOICES = [
#     ('ngo', 'NGO'),
#     ('research', 'Research Group'),
#     # add more if needed
# ]

# class RegistrationForm(forms.Form):
#     role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select, required=True)
#     name = forms.CharField(max_length=100, required=True)
#     email = forms.EmailField(required=True)
#     username = forms.CharField(max_length=100, required=True)
#     phone = forms.CharField(max_length=15, required=True)
#     password = forms.CharField(widget=forms.PasswordInput, required=True)
#     confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
#     org_type = forms.ChoiceField(choices=ORG_TYPE_CHOICES, required=False)
#     address = forms.CharField(widget=forms.Textarea, required=False)

#     def clean(self):
#         cleaned_data = super().clean()
#         pwd = cleaned_data.get("password")
#         cpwd = cleaned_data.get("confirm_password")
#         if pwd and cpwd and pwd != cpwd:
#             raise forms.ValidationError("Passwords do not match")
#         return cleaned_data


# class OTPVerificationForm(forms.Form):
#     otp = forms.CharField(max_length=6, required=True)
