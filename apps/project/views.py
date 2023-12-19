from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response

from base.permissions import ModulePermission
from base.renderers import ApiRenderer
from .models import Project, ProjectMember
from .serializers import ProjectMemberSerializer, ProjectSerializer
from django_filters.rest_framework import DjangoFilterBackend
from common.helpers import module_perm
from common.constants import ApplicationMessages


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [ModulePermission]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]  # Add DjangoFilterBackend
    render_classes = [ApiRenderer]
    filterset_fields = [
        "id",
        "project_name",
        "start_date",
        "end_date",
        "project_type",
    ]  # Define the fields available for filtering

    # Define fields available for filtering and ordering
    ordering_fields = ["project_name", "start_date", "end_date"]
    search_fields = ["project_name", "project_code", "notes"]

    def get_queryset(self):
        # Filter projects by the user's company
        user = self.request.user
        return Project.objects.filter(company_id=user.company_id)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": ApplicationMessages.SUCCESS,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Update the 'company_id' field
        instance = serializer.instance
        instance.company_id = request.user.company_id
        instance.save()

        return Response(
            {
                "status": status.HTTP_201_CREATED,
                "message": ApplicationMessages.SUCCESS,
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
                "data": {},
            },
            status=status.HTTP_200_OK,
        )


class ProjectMemberViewSet(viewsets.ModelViewSet):
    permission_classes = [ModulePermission]
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]  # Add DjangoFilterBackend
    render_classes = [ApiRenderer]
    filterset_fields = [
        "id",
        "project",
        "member",
    ]  # Define the fields available for filtering

    # Define fields available for filtering and ordering
    ordering_fields = [
        "project",
        "member",
    ]
    search_fields = [
        "project",
        "member",
    ]

    def get_queryset(self):
        # Filter projects by the user's company
        user = self.request.user
        return ProjectMember.objects.filter(
            project__company_id=user.company_id
        )

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": ApplicationMessages.SUCCESS,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                "status": status.HTTP_201_CREATED,
                "message": ApplicationMessages.SUCCESS,
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
                "data": {},
            },
            status=status.HTTP_200_OK,
        )
