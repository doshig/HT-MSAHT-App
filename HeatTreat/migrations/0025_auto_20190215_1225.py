# Generated by Django 2.1.4 on 2019-02-15 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeatTreat', '0024_auto_20190215_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specSoakMinusTimeTol',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
