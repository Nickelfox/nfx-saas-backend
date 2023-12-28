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


class Days_choice(TextChoices):
    """
    List of work day choices
    """

    MON = ("MON", "Monday")
    TUE = ("TUE", "Tuesday")
    WED = ("WED", "Wednesday")
    THU = ("THU", "Thursday")
    FRI = ("FRI", "Friday")
    SAT = ("SAT", "Saturday")
    SUN = ("SUN", "Sunday")


class Project_type(TextChoices):
    """
    List of Project types
    """

    VARIABLE = ("VARIABLE", "Variable By Hour")
    FIXED = ("FIXED", "Fixed Fee")
    NON_BILLABLE = ("NON_BILLABLE", "Non Billable")


class Color_choice(TextChoices):
    """
    List of Project Color Code choices
    """

    Orange = ("#fa6400cc", "Orange")
    Green = ("#1e8c0acc", "Green")
    Aqua = ("#3ca0c8cc", "Aqua")
    Blue = ("#004696cc", "Blue")
    Purple = ("#78328ccc", "Purple")
    Magenta = ("#d22864cc", "Magenta")
    Red = ("#d20a0acc", "Red")
    Gray = ("#888888cc", "Gray")


class Schedule_type(TextChoices):
    WORK = ("WORK", "Work")
    TIME_OFF = ("TIME_OFF", "Time Off")


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
    EMAIL_PASSWORD_INCORRECT = "Invalid Email Or Password"
    INVALID_PASSWORD = "Invalid Email Or Password"
    INVALID_EMAIL = "You are not logged in with the same email id".title()
    LOGIN_SUCCESSFULLY = "login successful".title()
    LOGOUT_SUCCESSFULLY = "Logout is successful".title()
    LOGOUT_FAILED_NO_TOKEN = "Logout Failed. No Active Login found".title()
    LOGOUT_FAILED = "Logout Failed. No Active User found".title()
    USER_NOT_ACTIVE = "User is not active".title()
    SUCCESS = "Success"
    PERMISSION_DENIED = "Permission denied for this operation.".title()
    DELETED_SUCCESS = "Object deleted successfully.".title()


class GeneralConstants:
    """
    General constant values like passwords, names etc.
    """
    DEFAULT_PASSWORD = "Querty1234"
    NO_ACCESS_ROLE = "no_access_role"
    DEFAULT_WORK_DAYS = "MON,TUE,WED,THU,FRI"
    DEFAULT_WORK_CAPACITY = "8"
