# Generated by Django 3.2.5 on 2022-09-26 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dent', '0003_alter_appointment_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.TimeField(),
        ),
    ]