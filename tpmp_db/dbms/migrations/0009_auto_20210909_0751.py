# Generated by Django 3.2.7 on 2021-09-09 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbms', '0008_auto_20210908_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysisresult',
            name='filename',
            field=models.CharField(max_length=65536, unique=True),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='guid',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cameraconfigurationfile',
            name='filename',
            field=models.CharField(max_length=65536, unique=True),
        ),
        migrations.AlterField(
            model_name='datain',
            name='filename',
            field=models.CharField(max_length=65536, unique=True),
        ),
        migrations.AlterField(
            model_name='measure',
            name='guid',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='guid',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
