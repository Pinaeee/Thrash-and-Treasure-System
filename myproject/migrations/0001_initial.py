# Generated by Django 4.2.18 on 2025-02-10 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('courier_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('dp_name', models.CharField(max_length=100)),
                ('dp_phone_number', models.CharField(max_length=15)),
                ('courier_company', models.CharField(default='Unknown', max_length=50)),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Busy', 'Busy')], default='Available', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryReport',
            fields=[
                ('report_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('coordinator_id', models.CharField(default='DC001', max_length=10)),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('total_deliveries', models.IntegerField(default=0)),
                ('successful_deliveries', models.IntegerField(default=0)),
                ('pending_deliveries', models.IntegerField(default=0)),
                ('total_issues', models.IntegerField(default=0)),
                ('report_content', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('shipping_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('shipping_status', models.CharField(choices=[('Unassigned', 'Unassigned'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='Unassigned', max_length=20)),
                ('courier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.courier')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.order')),
            ],
        ),
        migrations.CreateModel(
            name='Issues',
            fields=[
                ('issue_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('issue_description', models.TextField()),
                ('issue_status', models.CharField(choices=[('Pending', 'Pending'), ('Resolved', 'Resolved'), ('Escalated', 'Escalated')], default='Pending', max_length=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.order')),
            ],
        ),
    ]
