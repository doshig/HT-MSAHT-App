# Generated by Django 2.1.4 on 2019-01-22 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeatTreat', '0009_heattreat_couponinit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heattreat',
            name='partsCleaned',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='YES', max_length=3),
        ),
    ]
