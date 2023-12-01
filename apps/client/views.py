from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from .models import Client
from .serializers import ClientSerializer
from django_filters.rest_framework import DjangoFilterBackend
from common.helpers import module_perm
from common.constants import ApplicationMessages


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]  # Add DjangoFilterBackend
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
        return Client.objects.filter(company_id=user.company_id)

    def list(self, request):
        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "client", req_user, "view"
        ):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "status": ApplicationMessages.SUCCESS,
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
        req_user = request.user
        if req_user.is_company_owner or module_perm("client", req_user, "add"):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            instance = serializer.instance
            instance.company_id = request.user.company_id
            instance.save()

            return Response(
                {
                    "status": ApplicationMessages.SUCCESS,
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

        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "client", req_user, "view"
        ):
            serializer = self.get_serializer(instance)
            return Response(
                {
                    "status": ApplicationMessages.SUCCESS,
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

        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "client", req_user, "update"
        ):
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {
                    "status": ApplicationMessages.SUCCESS,
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

        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "client", req_user, "update"
        ):
            serializer = self.get_serializer(
                instance, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {
                    "status": ApplicationMessages.SUCCESS,
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

        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "client", req_user, "delete"
        ):
            self.perform_destroy(instance)
            return Response(
                {
                    "status": ApplicationMessages.SUCCESS,
                    "message": ApplicationMessages.DELETED_SUCCESS,
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
