from django_filters import rest_framework as filters
from .models import Project, ProjectMember
from django.db.models import Case, When, Value, CharField
from common.constants import Project_type


class ProjectFilter(filters.FilterSet):
    id = filters.UUIDFilter(field_name="id")
    client_id = filters.UUIDFilter(field_name="client_id")
    project_type = filters.ChoiceFilter(
        field_name="project_type",
        choices=Project_type.choices,
    )
    # project_name = filters.CharFilter(
    #     field_name="project_name", method="filter_project_name"
    # )

    # def filter_project_name(self, queryset, project_name, value):
    #     # Perform case-insensitive partial match on the 'name' field
    #     queryset = queryset.filter(project_name__icontains=value)

    #     # Order the queryset based on the position of the search term in the name
    #     queryset = queryset.annotate(
    #         name_index=Case(
    #             When(project_name__icontains=value, then=Value(1)),
    #             default=Value(2),
    #             output_field=CharField(),
    #         )
    #     ).order_by("name_index")

    class Meta:
        model = Project
        fields = ["id", "client_id", "project_type"]


class ProjectMemberFilter(filters.FilterSet):
    id = filters.UUIDFilter(field_name="id")
    project_id = filters.UUIDFilter(field_name="project_id")
    member_id = filters.UUIDFilter(field_name="member_id")
    # project_name = filters.CharFilter(
    #     field_name="project_name", method="filter_project_name"
    # )

    # def filter_project_name(self, queryset, project_name, value):
    #     # Perform case-insensitive partial match on the 'name' field
    #     queryset = queryset.filter(project_name__icontains=value)

    #     # Order the queryset based on the position of the search term in the name
    #     queryset = queryset.annotate(
    #         name_index=Case(
    #             When(project_name__icontains=value, then=Value(1)),
    #             default=Value(2),
    #             output_field=CharField(),
    #         )
    #     ).order_by("name_index")

    class Meta:
        model = ProjectMember
        fields = ["id", "member_id", "project_id"]
