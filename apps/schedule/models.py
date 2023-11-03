from django.db import models
from common.models import BaseModel
from apps.project.models import ProjectMember
import datetime

# Create your models here.
class Schedule(BaseModel):
    project_member = models.ForeignKey(ProjectMember, on_delete=models.CASCADE)
    start_at = models.DateField()
    end_at = models.DateField()
    notes = models.TextField()
    assigned_hour = models.DurationField(default=datetime.timedelta(hours=0))  # This defines effort as an interval field

    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.project_member.project.project_name} \
                - {self.project_member.member.full_name} - {self.id}"