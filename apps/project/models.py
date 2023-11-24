from django.db import models
from apps.team.models import Team
from common.constants import Project_type
from common.models import BaseModel
from apps.client.models import Client
from apps.company.models import Company

# Create your models here.


class Project(BaseModel):
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, null=True, blank=True
    )
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, null=True, blank=True
    )
    project_name = models.CharField(max_length=255)
    project_code = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    project_type = models.CharField(
        max_length=40,
        choices=Project_type.choices,
        default=None,  # choice list Department_choice
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["-created_at"]

    def __str__(self):
        """String representation of projects"""
        return "{} - {}".format(self.project_name, self.id)


class ProjectMember(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Project Member"
        verbose_name_plural = "Project Members"
        ordering = ["-created_at"]

    def __str__(self):
        """String representation of project members"""
        return "{} - {} - {}".format(
            self.project.project_name, self.member.user.full_name, self.id
        )
