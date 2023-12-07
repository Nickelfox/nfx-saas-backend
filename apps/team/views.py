from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response

from apps.team.filters import TeamFilter
from .models import Team
from .serializers import TeamSerializer, TeamListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from common.helpers import module_perm
from common.constants import ApplicationMessages


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    serializer_class_list = TeamListSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]  # Add DjangoFilterBackend
    filterset_fields = [
        "user",
        "department",
    ]  # Define the fields available for filtering

    # Define fields available for filtering and ordering
    ordering_fields = [
        "capacity",
        "work_days",
        "department",
    ]
    search_fields = [
        "user",
        "department",
    ]

    def get_queryset(self):
        # Filter projects by the user's company
        user = self.request.user
        return Team.objects.filter(company_id=user.company_id)

    def list(self, request):
        # Check if the user has permission to list projects
        req_user = request.user
        if req_user.is_company_owner or module_perm("team", req_user, "view"):
            queryset = self.filter_queryset(self.get_queryset()).order_by(
                "user__full_name"
            )
            start_date = request.query_params.get("start_date", None)
            end_date = request.query_params.get("end_date", None)
            serializer = self.serializer_class_list(
                queryset,
                many=True,
                context={"start_date": start_date, "end_date": end_date},
            )
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": ApplicationMessages.SUCCESS,
                    "error": False,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": status.HTTP_403_FORBIDDEN,
                    "message": ApplicationMessages.PERMISSION_DENIED,
                    "error": True,
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def create(self, request):
        # Check if the user has permission to add a project
        req_user = request.user
        if req_user.is_company_owner or module_perm("team", req_user, "add"):
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
                    "error": False,
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "status": status.HTTP_403_FORBIDDEN,
                    "message": ApplicationMessages.PERMISSION_DENIED,
                    "error": True,
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        # Check if the user has permission to retrieve this project
        req_user = request.user
        if req_user.is_company_owner or module_perm("team", req_user, "view"):
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
        else:
            return Response(
                {
                    "status": status.HTTP_403_FORBIDDEN,
                    "message": ApplicationMessages.PERMISSION_DENIED,
                    "error": True,
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def update(self, request, pk=None):
        instance = self.get_object()
        # Check if the user has permission to update this project
        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "team", req_user, "update"
        ):
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
        else:
            return Response(
                {
                    "status": status.HTTP_403_FORBIDDEN,
                    "message": ApplicationMessages.PERMISSION_DENIED,
                    "error": True,
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        # Check if the user has permission to partially update this project
        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "team", req_user, "update"
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
                    "error": False,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": status.HTTP_403_FORBIDDEN,
                    "message": ApplicationMessages.PERMISSION_DENIED,
                    "error": True,
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def destroy(self, request, pk=None):
        instance = self.get_object()
        # Check if the user has permission to delete this project
        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "team", req_user, "delete"
        ):
            self.perform_destroy(instance)
            return Response(
                {
                    "status": status.HTTP_204_NO_CONTENT,
                    "message": ApplicationMessages.SUCCESS,
                    "error": False,
                    "data": {},
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {
                    "status": status.HTTP_403_FORBIDDEN,
                    "message": ApplicationMessages.PERMISSION_DENIED,
                    "error": True,
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )
