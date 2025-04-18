# Generated by Django 5.2 on 2025-04-09 20:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Завод', 'Завод'), ('Дистрибьютор', 'Дистрибьютор'), ('Дилерский центр', 'Дилерский центр'), ('Крупная розничная сеть', 'Крупная розничная сеть'), ('Индивидуальный предприниматель', 'Индивидуальный предприниматель')], max_length=255)),
                ('level', models.IntegerField(blank=True, null=True)),
                ('supplier', models.CharField()),
                ('debt', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('network_node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='api.node')),
            ],
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('house_number', models.CharField(max_length=10)),
                ('network_node', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='api.node')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('release_date', models.DateField()),
                ('network_node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='api.node')),
            ],
        ),
    ]
