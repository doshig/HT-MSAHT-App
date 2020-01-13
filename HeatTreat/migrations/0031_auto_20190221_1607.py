# Generated by Django 2.1.4 on 2019-02-22 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeatTreat', '0030_auto_20190221_1041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='printcert',
            name='material',
        ),
        migrations.RemoveField(
            model_name='printcert',
            name='quenchMethodLoad10',
        ),
        migrations.RemoveField(
            model_name='printcert',
            name='quenchMethodLoad2',
        ),
        migrations.RemoveField(
            model_name='printcert',
            name='quenchMethodLoad3',
        ),
        migrations.RemoveField(
            model_name='printcert',
            name='quenchMethodLoad4',
        ),
        migrations.RemoveField(
            model_name='printcert',
            name='quenchMethodLoad5',
        ),
        migrations.RemoveField(
            model_name='printcert',
            name='quenchMethodLoad6',
        ),
        migrations.RemoveField(
            model_name='printcert',
            name='quenchMethodLoad7',
        ),
        migrations.RemoveField(
            model_name='printcert',
            name='quenchMethodLoad8',
        ),
        migrations.RemoveField(
            model_name='printcert',
            name='quenchMethodLoad9',
        ),
        migrations.AddField(
            model_name='printcert',
            name='PWABatchControl',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='printcert',
            name='PWAMCL',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]