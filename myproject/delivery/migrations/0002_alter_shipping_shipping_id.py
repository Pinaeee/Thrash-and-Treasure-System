# Generated by Django 4.2.18 on 2025-02-11 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping',
            name='shipping_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
