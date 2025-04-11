from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    NodeViewSet,
    ContactsViewSet,
    ProductViewSet,
    EmployeeViewSet,
    GenerateQRCodeAPIView,
)

router = DefaultRouter()
router.register(r"nodes", NodeViewSet)
router.register(r"contacts", ContactsViewSet)
router.register(r"products", ProductViewSet)
router.register(r"employees", EmployeeViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("generate_qr/", GenerateQRCodeAPIView.as_view(), name="generate_qr"),
]
