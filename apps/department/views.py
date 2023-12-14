from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response

from apps.department.filters import DepartmentFilter
from base.permissions import ModulePermission
from base.renderers import ApiRenderer
from .models import Department
from .serializers import DepartmentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from common.helpers import module_perm
from common.constants import ApplicationMessages


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [ModulePermission]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]  # Add DjangoFilterBackend
    filterset_class = DepartmentFilter
    render_classes = [ApiRenderer]
    filterset_fields = [
        "id",
        "name",
    ]  # Define the fields available for filtering

    # Define fields available for filtering and ordering
    ordering_fields = [
        "name",
    ]
    search_fields = [
        "id",
        "name",
    ]

    def get_queryset(self):
        user = self.request.user
        return Department.objects.filter(company_id=user.company_id)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": ApplicationMessages.SUCCESS,
                "error": False,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = serializer.instance
        instance.company_id = request.user.company_id
        instance.save()

        return Response(
            {
                "status": status.HTTP_201_CREATED,
                "message": ApplicationMessages.SUCCESS,
                "error": False,
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": ApplicationMessages.SUCCESS,
                "error": False,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": ApplicationMessages.SUCCESS,
                "error": False,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": ApplicationMessages.SUCCESS,
                "error": False,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": ApplicationMessages.DELETED_SUCCESS,
                "error": False,
                "data": {},
            },
            status=status.HTTP_200_OK,
        )
