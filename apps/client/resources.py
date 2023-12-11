from import_export import resources, fields
from apps.client.models import Client


class ClientResource(resources.ModelResource):
    class Meta:
        model = Client
        report_skipped = True
        raise_errors = False
        import_id_fields = ["id"]

    def before_import_row(self, row, **kwargs):
        # Set company_id for every row during import
        user = kwargs.get("user")
        name = row.get("name")
        company_id = user.company.id
        existing_client = Client.objects.filter(
            name=name, company_id=company_id
        ).first()

        if existing_client:
            # Update the existing instance
            row["id"] = existing_client.id
            return

        # Set company_id for every row during import
        row["company"] = user.company.id

    def before_save_instance(self, instance, using_transactions, dry_run):
        # Set the company foreign key based on the company_id
        instance.company_id = instance.company.id
