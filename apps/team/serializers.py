from rest_framework import serializers

from apps.project.serializers import ProjectMemberTeamListSerializer
from apps.user.serializers import UserListSerializer
from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            "id",
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
            "capacity",
            "department",
            "work_days",
            "user",
            "company",
            "project_members",
        )
