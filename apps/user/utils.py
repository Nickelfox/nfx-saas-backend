from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.signing import TimestampSigner

def generate_one_time_token(user):
    signer = TimestampSigner()
    token = signer.sign(user.email)
    return token

def send_invite_email_to_user(user):
    current_site = get_current_site(None)
    token = generate_one_time_token(user)  # Generate the one-time token
    invitation_url = reverse('admin_user_send_invitation', args=[user.pk])  # Corrected URL pattern name
    invite_link = f"http://{current_site}{invitation_url}?token={token}"

    send_mail(
        'Invitation to Set Your Password',
        f"""Hello!\n\nYou are invited to SquadSpot Admin Panel.
        \n\nTo set your password, please follow this link: {invite_link}""",
        'sender@example.com',
        [user.email],
        fail_silently=False,
    )
