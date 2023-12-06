from django_filters import rest_framework as filters
from .models import User
from django.db.models import Case, When, Value, CharField


class UserFilter(filters.FilterSet):
    id = filters.UUIDFilter(field_name="id")
    role_id = filters.UUIDFilter(field_name="role_id")
    full_name = filters.CharFilter(
        field_name="full_name", method="filter_full_name"
    )

    def filter_full_name(self, queryset, name, value):
        # Perform case-insensitive partial match on the 'name' field
        queryset = queryset.filter(full_name__icontains=value)

        # Order the queryset based on the position of the search term in the name
        queryset = queryset.annotate(
            name_index=Case(
                When(full_name__icontains=value, then=Value(1)),
                default=Value(2),
                output_field=CharField(),
            )
        ).order_by("name_index")
        return queryset

    class Meta:
        model = User
        fields = ["id", "full_name", "role_id"]
