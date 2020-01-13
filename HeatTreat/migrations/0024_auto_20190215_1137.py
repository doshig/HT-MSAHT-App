# Generated by Django 2.1.4 on 2019-02-15 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeatTreat', '0023_auto_20190212_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='solutiontreatspecs',
            name='mostCurrent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specCleaning',
            field=models.CharField(blank=True, default='Yes', max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specLoadTC',
            field=models.CharField(blank=True, default="YES (X2 FOR TMQ'S)", max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specPartsCleanedAfterQuench',
            field=models.CharField(blank=True, default='YES IF OIL QUENCHED', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTMQHeatHigh',
            field=models.PositiveSmallIntegerField(blank=True, default='50', null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTMQHeatLow',
            field=models.PositiveSmallIntegerField(blank=True, default='25', null=True),
        ),
    ]
