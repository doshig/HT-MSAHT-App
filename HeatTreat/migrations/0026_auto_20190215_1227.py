# Generated by Django 2.1.4 on 2019-02-15 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeatTreat', '0025_auto_20190215_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='VFMinusTimeTol',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
