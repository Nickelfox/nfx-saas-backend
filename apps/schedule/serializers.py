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