# Generated by Django 2.1.4 on 2019-02-11 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeatTreat', '0019_auto_20190207_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='heattreat',
            name='locked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solutiontreatspecs',
            name='specLocked',
            field=models.BooleanField(default=False),
        ),
    ]
