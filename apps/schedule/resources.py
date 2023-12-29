from import_export import resources
from common.constants import Color_choice
from .models import Schedule
from apps.project.models import ProjectMember, Project
from apps.team.models import Team


class ScheduleResource(resources.ModelResource):
    class Meta:
        model = Schedule
        report_skipped = True
        raise_errors = False
        import_id_fields = ["id"]

    import_errors = []  # List to store error messages for skipped rows

    def before_import_row(self, row, **kwargs):
        name = row.get("project_name")
        email = row.get("email")
        end_at = row.get("end_at")
        start_at = row.get("start_at")
        assigned_hour = row.get("assigned_hour")

        existing_project_member = ProjectMember.objects.filter(
            project__project_name=name, member__user__email=email
        ).first()
        if existing_project_member:
            sch_obj = Schedule.objects.filter(
                project_member_id=existing_project_member.id,
                start_at=start_at,
                end_at=end_at,
                assigned_hour=str(assigned_hour),
            ).first()
            if sch_obj:
                row["id"] = sch_obj.id
            else:
                row["project_member"] = existing_project_member.id
        else:
            project_obj = Project.objects.filter(project_name=name).first()
            team_obj = Team.objects.filter(user__email=email).first()
            if project_obj and team_obj:
                project_member_data = {
                    "project": project_obj,
                    "member": team_obj,
                }
                row["project_member"] = ProjectMember.objects.create(
                    **project_member_data
                ).id
        # was having excel formatting problem, that's why put string
        row["assigned_hour"] = str(row["assigned_hour"])

    def skip_row(self, instance, original, row=None, errors=None):
        if errors:
            instance.project_member.project.project_name = row.get(
                "project_name", None
            )
            instance.project_member.member.user.email = row.get("email", None)
            instance.end_at = row.get("end_at", None)
            instance.start_at = row.get("start_at", None)
            instance.assigned_hour = row.get("assigned_hour", None)
            instance.notes = row.get("notes", None)
        return True if errors else False
