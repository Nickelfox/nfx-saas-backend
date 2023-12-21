from rest_framework import serializers
from .models import Project, ProjectMember


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            "id",
            "project_name",
            "project_code",
            "client",
            "start_date",
            "end_date",
            "project_type",
            "notes",
        )


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = (
            "id",
            "project",
            "member",
        )


class ProjectMemberTeamListSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = ProjectMember
        fields = (
            "id",
            "project",
            "member",
        )
