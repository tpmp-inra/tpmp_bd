# Generated by Django 3.2.7 on 2021-09-09 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbms', '0009_auto_20210909_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cameraconfigurationfile',
            name='filename',
            field=models.FileField(unique=True, upload_to=''),
        ),
    ]
