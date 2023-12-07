from django_filters import rest_framework as filters
from .models import Schedule
from django.db.models import Case, When, Value, CharField


class ScheduleFilter(filters.FilterSet):
    id = filters.UUIDFilter(field_name="id")
    project_member_id = filters.UUIDFilter(field_name="project_member_id")

    class Meta:
        model = Schedule
        fields = ["id", "project_member_id"]
