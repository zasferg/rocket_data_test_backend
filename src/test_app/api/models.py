from django.db import models

# Create your models here.

class Node(models.Model):

    NAME_CHOICES = [
        ('Завод', 'Завод'),
        ('Дистрибьютор', 'Дистрибьютор'),
        ('Дилерский центр', 'Дилерский центр'),
        ('Крупная розничная сеть', 'Крупная розничная сеть'),
        ('Индивидуальный предприниматель', 'Индивидуальный предприниматель'),
    ]

    name = models.CharField(max_length=255, choices=NAME_CHOICES)
    level = models.IntegerField(blank=True, null=True)
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    debt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.level is None:
            highest_level = Node.objects.aggregate(max_level=models.Max('level'))['max_level']
            self.level = 0 if highest_level is None else highest_level + 1

        if self.level > 0:
            supplier_node = Node.objects.filter(level=self.level - 1).first()
            if supplier_node:
                self.supplier = supplier_node

        super(Node, self).save(*args, **kwargs)


    class Meta:

        verbose_name = "Звено"
        verbose_name_plural = "Звенья"



class Contacts(models.Model):
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    network_node = models.OneToOneField("Node", on_delete=models.CASCADE, related_name='contacts')


class Product(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()
    network_node = models.ForeignKey("Node", on_delete=models.CASCADE, related_name='products')


class Employee(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    network_node = models.ForeignKey("Node", on_delete=models.CASCADE, related_name='employees')


