# Generated by Django 2.1.4 on 2019-02-25 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeatTreat', '0034_auto_20190222_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='printcert',
            name='certSaved',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='printcert',
            name='certSavedNotes',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
