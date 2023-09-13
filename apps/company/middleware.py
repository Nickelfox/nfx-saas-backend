# from custom_admin import CompanyAdminSite

# class CompanyAdminMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.admin_site = CompanyAdminSite()  # Create an instance of your custom admin site

#     def __call__(self, request):
#         # Print a message to check if the middleware is running
#         print("\n--------------------------\n")
#         print("CompanyAdminMiddleware is running!")
#         print("\n--------------------------\n")

#         self.admin_site.request = request  # Set the request attribute for the admin site
#         response = self.get_response(request)
#         return response
