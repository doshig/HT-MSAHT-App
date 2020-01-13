# Generated by Django 2.1.4 on 2019-02-21 18:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeatTreat', '0029_auto_20190219_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrintCert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workOrder', models.CharField(max_length=50)),
                ('partNumber', models.CharField(blank=True, max_length=100, null=True)),
                ('partRev', models.CharField(blank=True, max_length=10, null=True)),
                ('customer', models.CharField(blank=True, max_length=50, null=True)),
                ('coupons', models.BooleanField(blank=True, default=True, null=True)),
                ('specNumber', models.CharField(blank=True, max_length=50, null=True)),
                ('specRevision', models.CharField(blank=True, max_length=50, null=True)),
                ('specMaterial', models.CharField(blank=True, max_length=50, null=True)),
                ('specMaterialSpec', models.CharField(blank=True, max_length=50, null=True)),
                ('specMaterialSpecRevision', models.CharField(blank=True, max_length=50, null=True)),
                ('material', models.CharField(blank=True, max_length=50, null=True)),
                ('quantityTotal', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('quantityLoad1', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('quantityLoad2', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('quantityLoad3', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('quantityLoad4', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('quantityLoad5', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('quantityLoad6', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('quantityLoad7', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('quantityLoad8', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('quantityLoad9', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('quantityLoad10', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('PO', models.CharField(blank=True, max_length=100, null=True)),
                ('heatNumber', models.CharField(blank=True, max_length=20, null=True)),
                ('weightTotal', models.PositiveIntegerField(blank=True, null=True)),
                ('weightLoad1', models.PositiveIntegerField(blank=True, null=True)),
                ('weightLoad2', models.PositiveIntegerField(blank=True, null=True)),
                ('weightLoad3', models.PositiveIntegerField(blank=True, null=True)),
                ('weightLoad4', models.PositiveIntegerField(blank=True, null=True)),
                ('weightLoad5', models.PositiveIntegerField(blank=True, null=True)),
                ('weightLoad6', models.PositiveIntegerField(blank=True, null=True)),
                ('weightLoad7', models.PositiveIntegerField(blank=True, null=True)),
                ('weightLoad8', models.PositiveIntegerField(blank=True, null=True)),
                ('weightLoad9', models.PositiveIntegerField(blank=True, null=True)),
                ('weightLoad10', models.PositiveIntegerField(blank=True, null=True)),
                ('loadsTotal', models.IntegerField(blank=True, default=1, null=True)),
                ('specTempLow', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('specTempHigh', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('specSoakTime', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('specSoakMinusTimeTol', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('specSoakPosTimeTol', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('furnaceNoLoad1', models.CharField(blank=True, max_length=50, null=True)),
                ('soakTempLoad1', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('soakTempLoad2', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('soakTempLoad3', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('soakTempLoad4', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('soakTempLoad5', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('soakTempLoad6', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('soakTempLoad7', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('soakTempLoad8', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('soakTempLoad9', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('soakTempLoad10', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('soakTimeStartLoad1', models.TimeField(blank=True, null=True)),
                ('soakTimeStartLoad2', models.TimeField(blank=True, null=True)),
                ('soakTimeStartLoad3', models.TimeField(blank=True, null=True)),
                ('soakTimeStartLoad4', models.TimeField(blank=True, null=True)),
                ('soakTimeStartLoad5', models.TimeField(blank=True, null=True)),
                ('soakTimeStartLoad6', models.TimeField(blank=True, null=True)),
                ('soakTimeStartLoad7', models.TimeField(blank=True, null=True)),
                ('soakTimeStartLoad8', models.TimeField(blank=True, null=True)),
                ('soakTimeStartLoad9', models.TimeField(blank=True, null=True)),
                ('soakTimeStartLoad10', models.TimeField(blank=True, null=True)),
                ('soakTimeEndLoad1', models.TimeField(blank=True, null=True)),
                ('soakTimeEndLoad2', models.TimeField(blank=True, null=True)),
                ('soakTimeEndLoad3', models.TimeField(blank=True, null=True)),
                ('soakTimeEndLoad4', models.TimeField(blank=True, null=True)),
                ('soakTimeEndLoad5', models.TimeField(blank=True, null=True)),
                ('soakTimeEndLoad6', models.TimeField(blank=True, null=True)),
                ('soakTimeEndLoad7', models.TimeField(blank=True, null=True)),
                ('soakTimeEndLoad8', models.TimeField(blank=True, null=True)),
                ('soakTimeEndLoad9', models.TimeField(blank=True, null=True)),
                ('soakTimeEndLoad10', models.TimeField(blank=True, null=True)),
                ('SoakTimeLoad1', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('SoakTimeLoad2', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('SoakTimeLoad3', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('SoakTimeLoad4', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('SoakTimeLoad5', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('SoakTimeLoad6', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('SoakTimeLoad7', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('SoakTimeLoad8', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('SoakTimeLoad9', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('SoakTimeLoad10', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('quenchMethodLoad1', models.CharField(blank=True, default=' ', max_length=5, null=True)),
                ('quenchMethodLoad2', models.CharField(blank=True, default=' ', max_length=5, null=True)),
                ('quenchMethodLoad3', models.CharField(blank=True, default=' ', max_length=5, null=True)),
                ('quenchMethodLoad4', models.CharField(blank=True, default=' ', max_length=5, null=True)),
                ('quenchMethodLoad5', models.CharField(blank=True, default=' ', max_length=5, null=True)),
                ('quenchMethodLoad6', models.CharField(blank=True, default=' ', max_length=5, null=True)),
                ('quenchMethodLoad7', models.CharField(blank=True, default=' ', max_length=5, null=True)),
                ('quenchMethodLoad8', models.CharField(blank=True, default=' ', max_length=5, null=True)),
                ('quenchMethodLoad9', models.CharField(blank=True, default=' ', max_length=5, null=True)),
                ('quenchMethodLoad10', models.CharField(blank=True, default=' ', max_length=5, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='soakTime',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='VFPHTSetPointHigh',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='VFPHTSetPointLow',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='VFPHTSetPointPref',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='VFPlusTimeTol',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='VFSoak',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='VFSoakPref',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specSoakMinusTimeTol',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specSoakPosTimeTol',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specSoakTime',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specSoakTimePref',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTMQHeatHigh',
            field=models.PositiveSmallIntegerField(blank=True, default='50', null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTMQHeatLow',
            field=models.PositiveSmallIntegerField(blank=True, default='25', null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTempAfterQuenchMax',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTempBeforeQuenchHigh',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTempBeforeQuenchLow',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTempSetPointHigh',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTempSetPointLow',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTempSetPointPref',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specTitaniumQuenchDelayMax',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specUniformityTol',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specUniformityTolPref',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='solutiontreatspecs',
            name='specVFVacPressure',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
