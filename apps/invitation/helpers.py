from apps.user.models import User


def reinvite_user(invitation):
    user_obj = User.objects.filter(email=invitation.email)
    if user_obj:
        user_obj.delete()
    invitation.is_active = True
    invitation.save()
