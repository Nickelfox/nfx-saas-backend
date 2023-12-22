# serializers.py
from rest_framework import serializers
from .models import Schedule
from .utils import working_days


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
    total_assigned_hours = serializers.SerializerMethodField()

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
            "total_assigned_hours",
        ]

    def get_assigned_hours(self, obj):
        # TODO:some model level changes need to be made to assigned hour, to optimize this
        if (obj.assigned_hour.microseconds//10000) > 0:
            minute_part = obj.assigned_hour.microseconds//10000
            return minute_part/100 + obj.assigned_hour.seconds
        return int(obj.assigned_hour.total_seconds()) if obj.assigned_hour else 0

    
    def get_total_assigned_hours(self, obj):
        if obj.project_member.member.work_days:
            working_days_num = len(
                working_days(obj.start_at, obj.end_at, obj.project_member.member.work_days)
                )
            return working_days_num * self.get_assigned_hours(obj)
        return 0
