# Generated by Django 2.1.4 on 2019-01-07 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeatTreat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('materialName', models.CharField(max_length=100)),
                ('field1', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Operators',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operatorName', models.CharField(max_length=100)),
                ('field1', models.CharField(blank=True, max_length=100, null=True)),
                ('field2', models.CharField(blank=True, max_length=100, null=True)),
                ('field3', models.CharField(blank=True, max_length=100, null=True)),
                ('field4', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SolutionTreatSpecs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specNumber', models.CharField(max_length=50)),
                ('specRevision', models.CharField(max_length=50)),
                ('specMaterial', models.CharField(max_length=50)),
                ('specMaterialSpec', models.CharField(max_length=50)),
                ('specMaterialSpecRevision', models.CharField(max_length=50)),
                ('specVF1', models.BooleanField(blank=True)),
                ('specVF2', models.BooleanField(blank=True)),
                ('specTMQ1', models.BooleanField(blank=True)),
                ('specTMQ2', models.BooleanField(blank=True)),
                ('specTMQ3', models.BooleanField(blank=True)),
                ('specCleaning', models.BooleanField(blank=True)),
                ('specTempSetPointLow', models.PositiveSmallIntegerField(blank=True)),
                ('specTempSetPointHigh', models.PositiveSmallIntegerField(blank=True)),
                ('specUniformityTol', models.PositiveSmallIntegerField(blank=True)),
                ('specSoakTime', models.PositiveSmallIntegerField(blank=True)),
                ('specSoakMinusTimeTol', models.PositiveSmallIntegerField(blank=True)),
                ('specSoakPosTimeTol', models.PositiveSmallIntegerField(blank=True)),
                ('specVFVacPressure', models.PositiveSmallIntegerField(blank=True)),
                ('specTMQHeatLow', models.PositiveSmallIntegerField(blank=True)),
                ('specTMQHeatHigh', models.PositiveSmallIntegerField(blank=True)),
                ('specLoadTC', models.CharField(blank=True, max_length=50)),
                ('specQuenchGFC', models.BooleanField(blank=True)),
                ('specQuenchOil', models.BooleanField(blank=True)),
                ('specQuenchWater', models.BooleanField(blank=True)),
                ('specQuenchAir', models.BooleanField(blank=True)),
                ('specTempBeforeQuenchLow', models.IntegerField(blank=True)),
                ('specTempBeforeQuenchHigh', models.IntegerField(blank=True)),
                ('specTempAfterQuenchMax', models.PositiveSmallIntegerField(blank=True)),
                ('specTitaniumQuenchDelayMax', models.PositiveSmallIntegerField(blank=True)),
                ('specPartsCleanedAfterQuench', models.CharField(blank=True, max_length=50)),
                ('specMasterReviewed', models.CharField(blank=True, max_length=50)),
                ('specMasterApproved', models.CharField(blank=True, max_length=50)),
                ('specFormRevision', models.PositiveSmallIntegerField(blank=True)),
                ('specFormRevDate', models.DateField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specCleaning',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specFormRevDate',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specFormRevision',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specLoadTC',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specMasterApproved',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specMasterReviewed',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specPartsCleanedAfterQuench',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specQuenchAir',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specQuenchGFC',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specQuenchOil',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specQuenchWater',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specSoakMinusTimeTol',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specSoakPosTimeTol',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specSoakTime',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specTMQ1',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specTMQ2',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specTMQ3',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specTMQHeatHigh',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specTMQHeatLow',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specTempAfterQuenchMax',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specTempBeforeQuenchHigh',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specTempBeforeQuenchLow',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specTempSetPointHigh',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specTempSetPointLow',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specTitaniumQuenchDelayMax',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specUniformityTol',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specVF1',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specVF2',
        ),
        migrations.RemoveField(
            model_name='heattreat',
            name='specVFVacPressure',
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='PWABatchControl',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='PWAMCL',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='TMQHeatEnv',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='TMQTenPurge',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='VFVacPressure',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='WQuenchDelay',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='agitReq',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='channelOne',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='channelTwo',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='cleaningReq',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='dateTimeIn',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='dateTimeOut',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='furnaceNo',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='genBy',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='genDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='goodCond',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='numPans',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='operatorIn',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='operatorOut',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='partialPressure',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='partsCleaned',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='preHeatEnd',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='preHeatStart',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='quantityLot',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='quenchMethod',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='reviewBy',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='reviewDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='soakTime',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='soakTimeEnd',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='soakTimeMinusTol',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='soakTimePlusTol',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='soakTimeStart',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='tempAfterQuench',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='tempBeforeQuench',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='tempSetPoint',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='tempSetPointHigh',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='tempSetPointLow',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='uniformityTol',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='heattreat',
            name='weightLot',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
