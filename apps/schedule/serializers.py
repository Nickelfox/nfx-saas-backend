# serializers.py
from rest_framework import serializers
from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = [
            "id",
            "project_member",
            "start_at",
            "end_at",
            "notes",
            "assigned_hour",
            "schedule_type",
        ]


class SchedulelistSerializer(serializers.ModelSerializer):
    project_id = serializers.CharField(source="project_member.project_id")
    department_id = serializers.UUIDField(
        source="project_member.member.department_id"
    )
    department_name = serializers.CharField(
        source="project_member.member.department.name"
    )

    class Meta:
        model = Schedule
        fields = [
            "id",
            "project_member",
            "project_id",
            "department_id",
            "department_name",
            "start_at",
            "end_at",
            "notes",
            "assigned_hour",
            "schedule_type",
        ]
