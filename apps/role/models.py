from django.db import models
from apps.company.models import Company
from common.models import BaseModel
# Define the choices for RoleModule as a tuple of tuples
ROLE_MODULE_CHOICES = (
    ("USERS", "USERS"),
    ("ROLES", "ROLES"),
    ("COMPANIES", "COMPANIES"),
    ("INVITATIONS", "INVITATIONS"),
    # Add more modules here as needed
)
ROLE_PERMISSION_CHOICES = [
    ("add", "Add"),
    ("view", "View"),
    ("update", "Update"),
    ("delete", "Delete"),
]

class AccessRole(BaseModel):
    """Create a single model for role management"""

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    role_permissions = models.JSONField(default=dict)

    class Meta:
        verbose_name = "Access Role"
        verbose_name_plural = "Access Roles"
        ordering = ["-created_at"]

    def __str__(self):
        """String representation of roles"""
        return "{} - {}".format(self.name, self.id)

