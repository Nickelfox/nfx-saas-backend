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
    project_id = serializers.UUIDField(source="project_member.project_id")
    member_id = serializers.UUIDField(source="project_member.member_id")
    assigned_hours = serializers.SerializerMethodField(source="assigned_hour")

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
            "member_id",
            "department_id",
            "department_name",
            "start_at",
            "end_at",
            "notes",
            "assigned_hours",
            "schedule_type",
        ]

    def get_assigned_hours(self, obj):
        return (
            int(obj.assigned_hour.total_seconds())
            if obj.assigned_hour
            else None
        )
