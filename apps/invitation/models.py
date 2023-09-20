from django.db import models
from common.models import BaseModel
from common.constants import Invite_type
from apps.role.models import AccessRole
import uuid

# Create your models here.


class Invitation(BaseModel):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=False, null=False)
    role = models.ForeignKey(
        AccessRole, on_delete=models.CASCADE, null=True, blank=True
    )
    invite_link = models.URLField(default="", blank=True)
    invite_type = models.CharField(
        max_length=20,
        choices=Invite_type.choices,  # Use the choices from Invite_type
        default=Invite_type.INTERNAL,  # Set a default choice if needed
    )
    company_id = models.UUIDField(
        default=uuid.uuid4, editable=False, blank=True, null=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"""{self.fullname} ({self.email}) {self.role.name}"""
