from django.db import models
from common.models import BaseModel
from apps.company.models import Company

# Create your models here.


class Department(BaseModel):
    """
    Department model is to specify the name of departments
    """

    name = models.CharField(
        max_length=255, null=False, blank=False, unique=True
    )
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, null=True, blank=True
    )

    def __str__(self):
        """
        String representation
        :return:
        """
        return "{}".format(self.name)
