from django.db import models
from common.models import BaseModel
from apps.company.models import Company

# Define the choices for RoleModule as a tuple of tuples


class AccessRole(BaseModel):
    """Create a single model for role management"""

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    role_permissions = models.JSONField(default=dict)
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        verbose_name = "Access Role"
        verbose_name_plural = "Access Roles"
        ordering = ["-created_at"]

    def __str__(self):
        """String representation of roles"""
        return "{} - {}".format(self.name, self.id)
