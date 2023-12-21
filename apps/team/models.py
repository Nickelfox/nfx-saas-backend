from django.db import models
from apps.company.models import Company
from apps.department.models import Department
from apps.user.models import User
from common.constants import Days_choice
from common.models import BaseModel
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Team(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emp_id = models.CharField(max_length=255, blank=True, null=True)
    capacity = models.DurationField()  # Use DurationField for hours per week
    work_days = ArrayField(
        models.CharField(max_length=3, choices=Days_choice.choices),
        size=7,
    )  # Assuming it represents days of the week (e.g., "MTWTFSS")
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.full_name} - {self.emp_id}"
