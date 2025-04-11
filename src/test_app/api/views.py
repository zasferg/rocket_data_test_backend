from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Node, Contacts, Product, Employee
from .serializers import (
    NodeGetSerializer,
    NodeCreateSerializer,
    ContactsSerializer,
    ProductSerializer,
    EmployeeSerializer,
)
from django.db.models import Avg
from rest_framework.views import APIView
from api.tasks import send_mail_with_qr


class NodeViewSet(viewsets.ModelViewSet):

    queryset = Node.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return NodeCreateSerializer
        return NodeGetSerializer

    @action(detail=False, methods=["get"], url_path="nodes_country/(?P<country>[^/.]+)")
    def nodes_by_country(self, request, country=None):
        if country is None:
            return Response(
                {"error": "Parameter 'country' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        nodes = Node.objects.filter(contacts__country__icontains=country)
        serializer = self.get_serializer(nodes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="debt-statistics")
    def debt_statistics(self, request):
        average_debt = Node.objects.aggregate(avg_debt=Avg("debt"))["avg_debt"]
        nodes = Node.objects.filter(debt__gt=average_debt)
        serializer = self.get_serializer(nodes, many=True)
        return Response(serializer.data)

    @action(
        detail=False, methods=["get"], url_path="nodes_product/(?P<product_id>[^/.]+)"
    )
    def nodes_by_product(self, request, product_id=None):
        if product_id is None:
            return Response(
                {"error": "Parameter 'product_id' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        nodes = Node.objects.filter(products__id=product_id)
        serializer = self.get_serializer(nodes, many=True)
        return Response(serializer.data)


class ContactsViewSet(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class GenerateQRCodeAPIView(APIView):
    def get(self, request):
        if not request.user.email:
            return Response(
                {"error": "Email и контактные данные обязательны."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }
        
        send_mail_with_qr.delay(request.user.email, data)
        return Response(
            {"message": "QR код будет отправлен на ваш email."},
            status=status.HTTP_200_OK,
        )
