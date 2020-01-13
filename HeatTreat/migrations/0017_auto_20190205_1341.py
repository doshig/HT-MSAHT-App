# Generated by Django 2.1.4 on 2019-02-05 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeatTreat', '0016_heattreat_timein'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='VFMinusTimeTol',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='VFPHTSetPointHigh',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='VFPHTSetPointLow',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='VFPHTSetPointPref',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='VFPlusTimeTol',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='VFSoak',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='VFSoakPref',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specCleaning',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specFormRevDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specFormRevision',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specLoadTC',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specMasterApproved',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specMasterReviewed',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specPartsCleanedAfterQuench',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specQuenchAir',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specQuenchGFC',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specQuenchOil',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specQuenchWater',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specSoakMinusTimeTol',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specSoakPosTimeTol',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specSoakTime',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specSoakTimePref',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTMQ1',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTMQ2',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTMQ3',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTMQHeatHigh',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTMQHeatLow',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTempAfterQuenchMax',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTempBeforeQuenchHigh',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTempBeforeQuenchLow',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTempSetPointHigh',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTempSetPointLow',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTempSetPointPref',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specUniformityTol',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specUniformityTolPref',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specVF1',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specVF2',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specVFVacPressure',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
