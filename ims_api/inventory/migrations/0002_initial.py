# Generated by Django 5.1.3 on 2025-01-07 14:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorychange',
            name='changed_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_changes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='inventory.category'),
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventorychange',
            name='inventory_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_changes', to='inventory.inventoryitem'),
        ),
    ]
