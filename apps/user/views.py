from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.signing import TimestampSigner, BadSignature
from django.contrib.auth import get_user_model
from .models import User, Invitation
from apps.company.models import Company
from common.helpers import get_object_from_models
from .utils import send_invite_email_to_user
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .forms import AcceptInvitationForm
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from custom_admin import company_admin_site

class CustomAdminLoginView(LoginView):
    template_name = 'admin/login.html'

    def get_success_url(self):
        # Check if the user is authenticated and has a company_name attribute
        if self.request.user.is_authenticated and hasattr(self.request.user, 'company'):
            company_name = self.request.user.company.name.lower()
            if company_name:
                # Set the site name dynamically
                company_admin_site.name = f"{company_name}-admin"
                # Redirect to the custom admin site with company_name
                return reverse_lazy('company_admin:index', kwargs={'company_name': company_name})

        # If conditions are not met, return the default admin URL
        return reverse_lazy('admin:index')


class AcceptInvitationView(FormView):
    template_name = 'user/accept_invitation.html'
    form_class = AcceptInvitationForm

    def get(self, request, uuid):
        model_name, obj = get_object_from_models(uuid)
        valid_flag = True
        if model_name and obj:
            if(model_name == "Invitation" and (not obj.is_active))or(model_name == "Company" and (obj.is_active)):
                valid_flag = False
                return HttpResponse("Invitation link expired")
        return render(request, self.template_name, {'form': self.form_class, 'invitation': obj, 'flag': valid_flag,})

    def post(self, request, uuid):
        # Retrieve the invitation associated with the UUID
        model_name, obj = get_object_from_models(uuid)
        if(model_name == "Invitation" and (not obj.is_active))or(model_name == "Company" and (obj.is_active)):
            return HttpResponse("Invitation link expired")
        
        # Create a new user with the provided email and password
        password = request.POST.get('password')
        encrpt_pswd = make_password(password)
        user = User.objects.create(
            full_name=obj.fullname if model_name == "Invitation" else obj.owner_name,
            email=obj.email if model_name == "Invitation" else obj.owner_email,
            role=obj.role if model_name == "Invitation" else None,
            company=obj if model_name == "Company" else None, 
            password=encrpt_pswd,
            is_staff = True,
            is_company_owner = True if model_name == "Company" else False,
            )

        # Associate the user with the invitation and mark it as accepted
        print(f"\n before : {obj.is_active}\n")
        obj.is_active = True if model_name == "Company" else False
        print(f"\n after : {obj.is_active}\n")
        obj.invite_link = None if model_name == "Company" else obj.invite_link
        obj.save()

        return redirect('user:password_set_success')  # Redirect to a success page


class PasswordSetSuccessView(TemplateView):
    template_name = 'user/set_password_template.html'
