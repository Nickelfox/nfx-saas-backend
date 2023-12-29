from datetime import timedelta
from import_export import resources

# from import_export.results import SkipRowException
from apps.user.models import User
from apps.role.models import AccessRole
from apps.department.models import Department
from .models import Team
from common.constants import GeneralConstants


class TeamResource(resources.ModelResource):
    class Meta:
        model = Team
        report_skipped = True
        raise_errors = False
        import_id_fields = ["id"]

    import_errors = []

    def before_import_row(self, row, **kwargs):
        # Set company_id for every row during import
        user = kwargs.get("user")
        company_id = user.company.id
        full_name = row.get("full_name", None)
        email = row.get("email", None)
        department_name = row.get("department", None)
        designation = row.get("designation")
        row_skip = False
        if email and department_name:
            existing_user = User.objects.filter(
                email=email,
                company_id=company_id,
            ).first()
            if existing_user:
                row["user"] = existing_user.id
            else:
                role, created = AccessRole.objects.get_or_create(
                    name="no_access_role", company_id=company_id
                )
                user_obj = User.objects.create_user(
                    email=email,
                    password=GeneralConstants.DEFAULT_PASSWORD,  # Set your default password here
                )
                user_obj.role_id = role.id
                user_obj.designation = designation
                user_obj.company_id = company_id
                user_obj.full_name = full_name
                user_obj.save()
                row["user"] = user_obj.id
            existing_department = Department.objects.filter(
                name=department_name, company_id=company_id
            ).first()
            if existing_department:
                row["department"] = existing_department.id
                existing_team = Team.objects.filter(
                    user=row["user"],
                    department_id=existing_department.id,
                    company_id=company_id,
                ).first()
                if existing_team:
                    row["id"] = existing_team.id
            else:
                row_skip = True
        else:
            row_skip = True
        row["company"] = user.company.id
        row["capacity"] = GeneralConstants.DEFAULT_WORK_CAPACITY
        row["work_days"] = GeneralConstants.DEFAULT_WORK_DAYS
        return row_skip

    def skip_row(self, instance, original, row=None, errors=None):
        if errors:
            instance.emp_id = row.get("emp_id", None)
        return True if errors else False

    def before_save_instance(self, instance, using_transactions, dry_run):
        # Set the company foreign key based on the company_id
        instance.company_id = instance.company.id if instance.company else None
