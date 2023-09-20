from django.db import models
from common.models import BaseModel

# Create your models here.


class Company(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    owner_name = models.CharField(max_length=255, null=False, blank=False)
    owner_email = models.CharField(max_length=255, null=False, blank=False)
    invite_link = models.URLField(default="", blank=True)
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
