# Generated by Django 5.0 on 2024-01-01 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_booking_adults_booking_children'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='check_in_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='check_out_date',
            field=models.DateField(null=True),
        ),
    ]
