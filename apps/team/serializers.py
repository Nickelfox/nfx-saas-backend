from rest_framework import serializers
from apps.department.serializers import DepartmentSerializer

from apps.project.serializers import (
    ProjectMemberTeamListSerializer,
)
from apps.schedule.utils import (
    calculate_weekly_assigned_hours,
    calculate_weekly_capacity,
)
from apps.user.serializers import UserListSerializer
from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            "id",
            "emp_id",
            "capacity",
            "department",
            "work_days",
            "user",
            "company",
        )


class TeamListSerializer(serializers.ModelSerializer):
    project_members = ProjectMemberTeamListSerializer(
        many=True, source="projectmember_set"
    )
    user = UserListSerializer()

    class Meta:
        model = Team
        fields = (
            "id",
            "emp_id",
            "capacity",
            "department",
            "work_days",
            "user",
            "company",
            "project_members",
        )


# class TimelineTeamSerializer(serializers.ModelSerializer):
#     user = UserListSerializer()
#     department = DepartmentSerializer()
#     project_members = ProjectMemberTeamListSerializer(
#         many=True, read_only=True
#     )
#     weekly_capacity = serializers.SerializerMethodField()
#     weekly_assigned_hours = serializers.SerializerMethodField()

#     class Meta:
#         model = Team
#         fields = "__all__"

#     def get_weekly_capacity(self, obj):
#         start_date = self.context["start_date"]
#         end_date = self.context["end_date"]
#         qs_schedule = self.context["qs_schedule"]
#         # Implement the logic to calculate weekly capacity
#         return calculate_weekly_capacity(obj, start_date, end_date)

#     def get_weekly_assigned_hours(self, obj):
#         start_date = self.context["start_date"]
#         end_date = self.context["end_date"]
#         qs_schedule = self.context["qs_schedule"]
#         # Implement the logic to calculate weekly assigned hours
#         return calculate_weekly_assigned_hours(
#             obj, start_date, end_date, qs_schedule
#         )
