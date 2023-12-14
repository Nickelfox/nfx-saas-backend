from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response

from apps.team.filters import TeamFilter
from base.permissions import ModulePermission
from base.renderers import ApiRenderer
from .models import Team
from .serializers import TeamSerializer, TeamListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from common.helpers import module_perm
from common.constants import ApplicationMessages


class TeamViewSet(viewsets.ModelViewSet):
    renderer_classes = [ApiRenderer]
    permission_classes = [ModulePermission]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    serializer_class_list = TeamListSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]  # Add DjangoFilterBackend
    filterset_class = TeamFilter
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
        queryset = self.filter_queryset(self.get_queryset())
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
                "message": ApplicationMessages.SUCCESS,
                "error": False,
                "data": {},
            },
            status=status.HTTP_200_OK,
        )
