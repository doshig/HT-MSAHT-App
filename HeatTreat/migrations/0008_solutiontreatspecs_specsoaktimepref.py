# Generated by Django 2.1.4 on 2019-01-22 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeatTreat', '0007_auto_20190122_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='solutiontreatspecs',
            name='specSoakTimePref',
            field=models.PositiveSmallIntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]