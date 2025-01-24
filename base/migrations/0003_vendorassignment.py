# Generated by Django 5.1.5 on 2025-01-24 07:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_rename_role_vendorcategory_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=100)),
                ('is_available', models.BooleanField(default=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.event')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.vendor')),
            ],
        ),
    ]
