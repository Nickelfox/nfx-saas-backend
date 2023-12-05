from django_filters import rest_framework as filters
from .models import Department
from django.db.models import Case, When, Value, CharField


class DepartmentFilter(filters.FilterSet):
    id = filters.UUIDFilter(field_name="id")
    name = filters.CharFilter(field_name="name", method="filter_name")

    def filter_name(self, queryset, name, value):
        # Perform case-insensitive partial match on the 'name' field
        queryset = queryset.filter(name__icontains=value)

        # Order the queryset based on the position of the search term in the name
        queryset = queryset.annotate(
            name_index=Case(
                When(name__icontains=value, then=Value(1)),
                default=Value(2),
                output_field=CharField(),
            )
        ).order_by("name_index")
        return queryset

    class Meta:
        model = Department
        fields = ["id", "name"]
