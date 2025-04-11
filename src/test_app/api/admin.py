from django.contrib import admin
from api.models import Node, Contacts, Product, Employee
from api.tasks import clear_debt_task

# Register your models here.


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "level",
        "debt",
        "supplier_name",
        "created_at",
        "contacts__city",
    )
    list_display_links = (
        "name",
        "supplier_name",
    )
    list_filter = ("contacts__city",)
    search_fields = ("name",)
    actions = ("clear_debt",)

    def supplier_name(self, obj):
        return obj.supplier.name if obj.supplier else "-"

    @admin.action(description="Обнулить задолженности")
    def clear_debt(self, request, queryset):
        if queryset.count() > 5:
            queriset_ids = list(queryset.values_list("id", flat=True))
            clear_debt_task.delay(ids=queriset_ids)
        else:
            queryset.update(debt=0)


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "country",
        "city",
        "street",
        "house_number",
        "network_node__name",
    )


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass
