from import_export import resources

# from import_export.results import SkipRowException
from .models import Project, Client, Company


class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project
        report_skipped = True
        raise_errors = False
        import_id_fields = ["id"]

    import_errors = []  # List to store error messages for skipped rows

    color_mapping = {
        "Warm Red": "#F10982",
        "Red": "#FF0000",
        "Orange": "#FF7034",
        "Maroon": "#800000",
        "Royal Blue": "#4169e1",
        "Light Green": "#57f287",
    }

    def before_import_row(self, row, **kwargs):
        # Set company_id for every row during import
        user = kwargs.get("user")
        company_id = user.company.id
        name = row.get("project_name")
        client_name = row.get("client")
        color_code_value = row.get("color_code")
        if color_code_value:
            row["color_code"] = self.color_mapping[color_code_value]
        existing_client = Client.objects.filter(
            name=client_name, company_id=company_id
        ).first()
        if existing_client:
            # Skip the row with a message

            row["client"] = existing_client.id
            existing_project = Project.objects.filter(
                project_name=name,
                client=existing_client.id,
                company_id=company_id,
            ).first()

            if existing_project:
                # Update the existing instance
                row["id"] = existing_project.id
        # Set company_id for every row during import
        row["company"] = user.company.id

    def skip_row(self, instance, original, row=None, errors=None):
        if errors:
            instance.project_name = row.get("project_name", None)
            instance.start_date = row.get("start_date", None)
            instance.end_date = row.get("end_date", None)
            instance.project_code = row.get("project_code", None)
            instance.color_code = row.get("color_code", None)
            instance.project_type = row.get("project_type", None)
            instance.client = None
        return True if errors else False

    def before_save_instance(self, instance, using_transactions, dry_run):
        # Set the company foreign key based on the company_id
        instance.company_id = instance.company.id if instance.company else None
