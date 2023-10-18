from django.db import models
from common.models import BaseModel
from apps.project.models import ProjectMember


# Create your models here.
class Schedule(BaseModel):
    project_member = models.ForeignKey(ProjectMember, on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    notes = models.TextField()
    status = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.project_member.project.project_name} \
                - {self.project_member.member.full_name} - {self.id}"
