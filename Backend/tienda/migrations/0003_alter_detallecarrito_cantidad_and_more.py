# Generated by Django 5.1.3 on 2024-11-20 18:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0002_alter_usuario_rol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallecarrito',
            name='cantidad',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='detallecarrito',
            name='carrito',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='tienda.carrito'),
        ),
        migrations.AlterField(
            model_name='detallecarrito',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles_carrito', to='tienda.producto'),
        ),
    ]
