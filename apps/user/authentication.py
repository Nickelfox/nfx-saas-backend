from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from apps.company.models import Company  # Import your Company model here

class SuperAdminBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            # Extract the company name from the email domain
            # flag, company_name = extract_company_name(user.email)

            # if flag:
            #     # Set a custom attribute in the user object to indicate the company
            #     user.company_name = company_name
            return user  # Return the user object

        return None


# def extract_company_name(email):
#     # Initialize the flag to False and company name to an empty string
#     flag = False
#     company_name = ""

#     # Split the email address at "@" to get the domain part
#     parts = email.split("@")
    
#     if len(parts) >= 2:
#         domain_name = parts[1]

#         # Check if the domain name is "sqsp.com"
#         if domain_name == "sqsp.com":
#             flag = True
#         else:
#             # Attempt to find the company name based on the email domain in your database
#             try:
#                 company_obj = Company.objects.get(owner_email__icontains=domain_name)
#                 company_name = company_obj.name.lower()
#             except Company.DoesNotExist:
#                 # Handle the case when no company is found for the domain
#                 pass

#     return flag, company_name
