from rest_framework import serializers
from .models import Project, ProjectMember


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            "id",
            "project_name",
            "project_code",
            "color_code",
            "client",
            "start_date",
            "end_date",
            "project_type",
            "notes",
        )


class ProjectMemberSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.project_name")
    member_name = serializers.CharField(source="member.user.full_name")

    class Meta:
        model = ProjectMember
        fields = (
            "id",
            "project",
            "project_name",
            "member",
            "member_name",
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
