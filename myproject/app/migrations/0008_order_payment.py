# Generated by Django 5.1.4 on 2025-02-02 20:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_item_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField()),
                ('order_status', models.CharField(max_length=50)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('payment_amount', models.FloatField()),
                ('payment_method', models.CharField(max_length=50)),
                ('payment_date', models.DateTimeField()),
                ('payment_status', models.CharField(max_length=50)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.order')),
            ],
        ),
    ]
