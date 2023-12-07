from import_export import resources

# from import_export.results import SkipRowException
from .models import Project, Client, Company


class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project
        import_id_fields = ["id"]

    def before_import_row(self, row, **kwargs):
        # Set company_id for every row during import
        user = kwargs.get("user")
        company_id = user.company.id
        client_name = row.get("client_name", None)

        if client_name:
            # try:
            client_obj = Client.objects.get(
                name=client_name, company=company_id
            )
            row["client"] = client_obj.id
            row["company"] = company_id
        #     except Client.DoesNotExist:
        #         raise SkipRowException(
        #             f"Client with name {client_name} does not exist."
        #         )

        # else:
        #     row["client"] = None

    def before_save_instance(self, instance, using_transactions, dry_run):
        # Set the company foreign key based on the company_id
        instance.company_id = instance.company.id if instance.company else None
        instance.client_id = instance.client.id if instance.client else None
