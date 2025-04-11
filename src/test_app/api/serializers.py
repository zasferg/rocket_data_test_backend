from rest_framework import serializers
from api.models import *


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class NodeGetSerializer(serializers.ModelSerializer):
    contacts = ContactsSerializer(many=False, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    employees = EmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = Node
        fields = "__all__"
        read_only_fields = ["debt"]


class NodeCreateSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True
    )

    class Meta:
        model = Node
        fields = ["name", "products"]
        read_only_fields = ["debt"]

    def create(self, validated_data):
        products_data = validated_data.pop("products")
        node = Node.objects.create(**validated_data)
        for product in products_data:
            node.products.add(product)
        return node

    def update(self, instance, validated_data):
        products_data = validated_data.pop("products")
        instance.name = validated_data.get("name", instance.name)
        instance.save()

        instance.products.clear()
        for product in products_data:
            instance.products.add(product)
        return instance
