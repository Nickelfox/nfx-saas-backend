from django.db import models
from common.models import BaseModel
from apps.company.models import Company

# Create your models here.


class Client(BaseModel):
    """Create a single model for client"""

    name = models.CharField(max_length=200, unique=True)
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ["-created_at"]

    def __str__(self):
        """String representation of clients"""
        return "{} - {}".format(self.name, self.id)
