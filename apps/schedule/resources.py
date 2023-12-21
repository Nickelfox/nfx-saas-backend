from import_export import resources
from datetime import timedelta
from common.constants import Color_choice
from .models import Schedule
from apps.project.models import ProjectMember, Project
from apps.team.models import Team
from datetime import timedelta

class ScheduleResource(resources.ModelResource):
    class Meta:
        model = Schedule
        report_skipped = True
        raise_errors = False
        import_id_fields = ["id"]

    import_errors = []  # List to store error messages for skipped rows

    def before_import_row(self, row, **kwargs):
        # Set company_id for every row during import
        user = kwargs.get("user")
        name = row.get("project_name")
        full_name = row.get("full_name")
        existing_project_member = ProjectMember.objects.filter(
            project__project_name=name, member__user__full_name=full_name
        ).first()
        if existing_project_member:
            row["project_member"] = existing_project_member.id
        else:
            project_member_data = {
                "project": Project.objects.filter(project_name=name).first(),
                "member": Team.objects.filter(user__full_name=full_name).first()

            }
            row["project_member"] = ProjectMember.objects.create(**project_member_data).id
        # was having excel formatting problem, that's why put string
        row["assigned_hour"] = str(row["assigned_hour"])

    def skip_row(self, instance, original, row=None, errors=None):
        if errors:
            instance.project_member.project.project_name = row.get("project_name", None)
            instance.project_member.member.user.full_name = row.get("full_name", None)
            instance.end_date = row.get("end_date", None)
            instance.assigned_hour = row.get("assigned_hour", None)
            instance.notes = row.get("notes", None)
        return True if errors else False

    # def before_save_instance(self, instance, using_transactions, dry_run):
    #     # Set the company foreign key based on the company_id
    #     instance.company_id = instance.company.id if instance.company else None
