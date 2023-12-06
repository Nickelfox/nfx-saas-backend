from import_export import resources, fields
from apps.client.models import Client


class ClientResource(resources.ModelResource):
    class Meta:
        model = Client
        import_id_fields = ["id"]

    def before_import_row(self, row, **kwargs):
        # Set company_id for every row during import
        user = kwargs.get("user")
        # row["id"] = uuid.uuid4()
        row["company"] = user.company.id

    def before_save_instance(self, instance, using_transactions, dry_run):
        # Set the company foreign key based on the company_id
        instance.company_id = instance.company.id
