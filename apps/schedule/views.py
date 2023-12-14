from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from apps.project.models import Project

from apps.schedule.utils import (
    calculate_working_days_project,
    calculate_working_days_team,
)
from apps.team.models import Team

from base.permissions import ModulePermission
from base.renderers import ApiRenderer
from .models import Schedule
from .serializers import ScheduleSerializer, SchedulelistSerializer
from django_filters.rest_framework import DjangoFilterBackend
from common.helpers import module_perm
from common.constants import ApplicationMessages
from datetime import datetime
from rest_framework import views
from apps.schedule.filters import ScheduleFilter
from base.renderers import ApiRenderer


# Create your views here.
class ScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [ModulePermission]
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    serializer_class_list = SchedulelistSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]  # Add DjangoFilterBackend
    render_classes = [ApiRenderer]
    filterset_class = ScheduleFilter
    filterset_fields = [
        "id",
        "project_member",
        "assigned_hour",
        "schedule_type",
    ]  # Define the fields available for filtering

    # Define fields available for filtering and ordering
    ordering_fields = [
        "start_at",
        "end_at",
        "assigned_hour",
    ]
    search_fields = [
        "id",
        "project_member",
        "start_at",
        "end_at",
    ]

    def get_queryset(self):
        # Filter projects by the user's company
        user = self.request.user
        return Schedule.objects.filter(
            project_member__project__company_id=user.company_id
        )

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        start_date = request.query_params.get("start_date", None)
        end_date = request.query_params.get("end_date", None)
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            queryset = queryset.filter(
                start_at__lte=end_date, end_at__gte=start_date
            )
        serializer = self.serializer_class_list(queryset, many=True)
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
        serializer = self.serializer_class_list(instance=serializer.instance)
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
        serializer = self.serializer_class_list(instance)
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
        serializer = self.serializer_class_list(instance=serializer.instance)
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
        serializer = self.serializer_class_list(instance=serializer.instance)
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
                "message": ApplicationMessages.SUCCESS,
                "data": {},
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class TimelineProjectAPIView(views.APIView):
    render_classes = [ApiRenderer]

    def get_queryset(self):
        # Filter projects by the user's company
        user = self.request.user
        return Project.objects.filter(company_id=user.company_id)

    def get(self, request):
        result = {}
        queryset = self.get_queryset()
        start_date = request.query_params.get("start_date", None)
        if start_date:
            result = calculate_working_days_project(start_date, queryset)
        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": ApplicationMessages.SUCCESS,
                "data": result,
            },
            status=status.HTTP_200_OK,
        )


class TimelineTeamAPIView(views.APIView):
    render_classes = [ApiRenderer]

    def get_queryset(self):
        # Filter projects by the user's company
        user = self.request.user
        return Team.objects.filter(company_id=user.company_id)

    def get(self, request):
        result = {}
        queryset = self.get_queryset()
        start_date = request.query_params.get("start_date", None)
        end_date = request.query_params.get("end_date", None)
        if start_date:
            result = calculate_working_days_team(
                start_date, end_date, queryset
            )
        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": ApplicationMessages.SUCCESS,
                "data": result,
            },
            status=status.HTTP_200_OK,
        )
