from django import forms
from apps.user.models import User


class AcceptInvitationForm(forms.Form):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)


# class UserAdminForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = (
#             'full_name', 
#             'email',
#             'role', 
#             'phone_number', 
#             'designation',
#             'company',
#             'is_company_owner',
#             )

#     def __init__(self, *args, **kwargs):
#         super(UserAdminForm, self).__init__(*args, **kwargs)
#         # Check if the ForeignKey field is null for the current instance
#         if self.instance and self.instance.role is None:
#             # Set the field as read-only
#             self.fields['role'].widget.attrs['readonly'] = True
#             self.fields['role'].widget.attrs['disabled'] = True
        
#         if self.instance and self.instance.company is None:
#             # Set the field as read-only
#             self.fields['company'].widget.attrs['readonly'] = True
#             self.fields['company'].widget.attrs['disabled'] = True