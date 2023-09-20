from django.db.models import TextChoices


class Invite_type(TextChoices):
    """
    Constants are written here and used in whole application
    """

    INTERNAL = ("Internal", "INTERNAL")
    COMPANY = ("Company", "COMPANY")
    COMPANY_OWNER = ("Company Owner", "COMPANY OWNER")


SQUAD_SPOT_ADMIN_ROUTE_NAME = "ss-admin"
COMPANY_ADMIN_ROUTE_NAME = "admin"


class ApplicationMessages:
    """
    Response, error etc application messages
    """

    COMPANY_INVALID = """
    You do not have permissions to access this page.
    Please Contact your Company Admin for further details.
    """
    INVITATION_INVALID = """
    Invitation link expired.
    Please Contact your Admin for valid invitation link."""
