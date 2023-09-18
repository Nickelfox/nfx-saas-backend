from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import User
from apps.company.models import Company
from common.helpers import get_object_from_models
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .forms import AcceptInvitationForm
from django.contrib.auth.hashers import make_password



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
        return render(request, self.template_name,
                      {'form': self.form_class,
                       'invitation': obj,
                       'flag': valid_flag,
                       })

    def post(self, request, uuid):
        # Retrieve the invitation associated with the UUID
        company_name = ""
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
            company_id=obj.company_id if obj.company_id is not None else None,
            password=encrpt_pswd,
            is_staff = True,
            is_company_owner = True if model_name == "Company" else False,
            )

        # Associate the user with the invitation and mark it as accepted
        obj.is_active = True if model_name == "Company" else False
        obj.invite_link = None if model_name == "Company" else obj.invite_link
        obj.save()
        if model_name == "Company":
            company_name = obj.name 
        elif obj.company_id is not None:
            com_obj = Company.objects.get(id=obj.company_id)
            company_name = com_obj.name  
            
        redirect_url = reverse('user:password_set_success')
        if company_name:
            redirect_url += f'?company_name={company_name}'

        return HttpResponseRedirect(redirect_url)  # Redirect to a success page


class PasswordSetSuccessView(TemplateView):
    template_name = 'user/set_password_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_name = self.request.GET.get('company_name')
        if company_name is not None:
            login_url = f'http://{company_name}.localhost:8000/admin'
        else:
            login_url= f'http://localhost:8000/ss-admin'
        context['login_url'] = login_url
        return context