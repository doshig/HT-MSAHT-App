# Generated by Django 2.1.4 on 2019-02-07 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeatTreat', '0017_auto_20190205_1341'),
    ]

    operations = [
        migrations.CreateModel(
            name='PolarChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yesNoChoice', models.CharField(max_length=3)),
            ],
        ),
    ]