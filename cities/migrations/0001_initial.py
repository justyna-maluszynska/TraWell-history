# Generated by Django 4.1.1 on 2022-11-11 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('county', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('lat', models.DecimalField(decimal_places=7, max_digits=15)),
                ('lng', models.DecimalField(decimal_places=7, max_digits=15)),
            ],
        ),
    ]
