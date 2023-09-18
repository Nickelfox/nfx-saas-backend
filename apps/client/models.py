from django.db import models
from common.models import BaseModel
import uuid
# Create your models here.

class Client(BaseModel):
    """Create a single model for client"""

    name = models.CharField(max_length=200, unique=True)
    company_id = models.UUIDField(default=uuid.uuid4, editable=False,blank=True, null=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ["-created_at"]

    def __str__(self):
        """String representation of clients"""
        return "{} - {}".format(self.name, self.id)

