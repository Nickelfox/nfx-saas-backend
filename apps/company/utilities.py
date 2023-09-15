

def get_tenant(request):
    company = request.user.company
    if company != None:
        return company.name
    else:
        return None
