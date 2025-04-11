import os
import django
from datetime import datetime
from faker import Faker


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_app.settings')
django.setup()

from api.models import Node, Contacts, Product, Employee

fake = Faker()

def create_nodes():
    name_factory = fake.random_element(elements=['Завод',])
    node = Node(name=name_factory, debt=0)
    node.save()
    for _ in range(99):
        name = fake.random_element(elements=['Дистрибьютор', 'Дилерский центр', 'Крупная розничная сеть', 'Индивидуальный предприниматель'])
        debt = fake.pydecimal(left_digits=5, right_digits=2, positive=True)
        node = Node(name=name, debt=debt)
        node.save()

def create_contacts():
    nodes = Node.objects.all()
    for node in nodes[:100]:
        email = fake.email()
        country = fake.country()
        city = fake.city()
        street = fake.street_name()
        house_number = fake.building_number()
        contact = Contacts(email=email, country=country, city=city, street=street, house_number=house_number, network_node=node)
        contact.save()

def create_products():
    nodes = Node.objects.all()
    for node in nodes[:100]:
        name = fake.word()
        model = fake.word()
        release_date = fake.date()
        product = Product(name=name, model=model, release_date=release_date, network_node=node)
        product.save()

def create_employees():
    nodes = Node.objects.all()
    for node in nodes[:100]:
        name = fake.name()
        position = fake.job()
        employee = Employee(name=name, position=position, network_node=node)
        employee.save()

if __name__ == "__main__":
    create_nodes()
    create_contacts()
    create_products()
    create_employees()
