from django.db import models
from common.models import BaseModel
from common.constants import Invite_type

# Create your models here.


class Company(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    owner_name = models.CharField(max_length=255, null=False, blank=False)
    owner_email = models.CharField(max_length=255, null=False, blank=False)
    invite_link = models.URLField(default="", blank=True)
    invite_type = models.CharField(
        max_length=20,
        choices=Invite_type.choices,  # Use the choices from Invite_type
        default=Invite_type.COMPANY_OWNER,  # Set a default choice if needed
    )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation
        :return:
        """
        return "{}-{}-{}".format(self.name, self.id, self.owner_email)

    class Meta:
        """
        Verbose name and verbose plural
        """

        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["-created_at"]
