from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response

from apps.project.filters import ProjectFilter, ProjectMemberFilter
from base.renderers import ApiRenderer
from .models import Project, ProjectMember
from .serializers import (
    ProjectMemberListSerializer,
    ProjectMemberSerializer,
    ProjectSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from common.helpers import module_perm
from common.constants import ApplicationMessages


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]  # Add DjangoFilterBackend
    render_classes = [ApiRenderer]
    filterset_class = ProjectFilter
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
        # Check if the user has permission to list projects
        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "project", req_user, "view"
        ):
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
        else:
            return Response(
                {
                    "status": "error",
                    "message": ApplicationMessages.PERMISSION_DENIED,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def create(self, request):
        # Check if the user has permission to add a project
        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "project", req_user, "add"
        ):
            # Get the user's company_id from the request user
            company_id = req_user.company.id
            # Serialize the data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            # Update the 'company_id' field
            instance = serializer.instance
            instance.company_id = (
                request.user.company_id
            )  # Assuming 'client' is a ForeignKey
            instance.save()

            return Response(
                {
                    "status": status.HTTP_201_CREATED,
                    "message": ApplicationMessages.SUCCESS,
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "status": "error",
                    "message": ApplicationMessages.PERMISSION_DENIED,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        # Check if the user has permission to retrieve this project
        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "project", req_user, "view"
        ):
            serializer = self.get_serializer(instance)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": ApplicationMessages.SUCCESS,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": "error",
                    "message": ApplicationMessages.PERMISSION_DENIED,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def update(self, request, pk=None):
        instance = self.get_object()
        # Check if the user has permission to update this project
        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "project", req_user, "update"
        ):
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
        else:
            return Response(
                {
                    "status": "error",
                    "message": ApplicationMessages.PERMISSION_DENIED,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        # Check if the user has permission to partially update this project
        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "project", req_user, "update"
        ):
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
        else:
            return Response(
                {
                    "status": "error",
                    "message": ApplicationMessages.PERMISSION_DENIED,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def destroy(self, request, pk=None):
        instance = self.get_object()
        # Check if the user has permission to delete this project
        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "project", req_user, "delete"
        ):
            self.perform_destroy(instance)
            return Response(
                {
                    "status": status.HTTP_204_NO_CONTENT,
                    "message": ApplicationMessages.DELETED_SUCCESS,
                    "data": {},
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {
                    "status": "error",
                    "message": ApplicationMessages.PERMISSION_DENIED,
                },
                status=status.HTTP_403_FORBIDDEN,
            )


class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    serializer_class_list = ProjectMemberListSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]  # Add DjangoFilterBackend
    render_classes = [ApiRenderer]
    filterset_class = ProjectMemberFilter
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
        # Check if the user has permission to list projects
        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "project_member", req_user, "view"
        ):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.serializer_class_list(queryset, many=True)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": ApplicationMessages.SUCCESS,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": "error",
                    "message": ApplicationMessages.PERMISSION_DENIED,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def create(self, request):
        # Check if the user has permission to add a project
        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "project_member", req_user, "add"
        ):
            # Get the user's company_id from the request user
            company_id = req_user.company.id
            # Serialize the data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": ApplicationMessages.SUCCESS,
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "status": "error",
                    "message": ApplicationMessages.PERMISSION_DENIED,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        # Check if the user has permission to retrieve this project
        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "project_member", req_user, "view"
        ):
            serializer = self.get_serializer(instance)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": ApplicationMessages.SUCCESS,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": "error",
                    "message": ApplicationMessages.PERMISSION_DENIED,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def update(self, request, pk=None):
        instance = self.get_object()
        # Check if the user has permission to update this project
        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "project_member", req_user, "update"
        ):
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
        else:
            return Response(
                {
                    "status": "error",
                    "message": ApplicationMessages.PERMISSION_DENIED,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        # Check if the user has permission to partially update this project
        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "project_member", req_user, "update"
        ):
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
        else:
            return Response(
                {
                    "status": "error",
                    "message": ApplicationMessages.PERMISSION_DENIED,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def destroy(self, request, pk=None):
        instance = self.get_object()
        # Check if the user has permission to delete this project
        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "project_member", req_user, "delete"
        ):
            self.perform_destroy(instance)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": ApplicationMessages.DELETED_SUCCESS,
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": "error",
                    "message": ApplicationMessages.PERMISSION_DENIED,
                },
                status=status.HTTP_403_FORBIDDEN,
            )
