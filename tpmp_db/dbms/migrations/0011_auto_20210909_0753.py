# Generated by Django 3.2.7 on 2021-09-09 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbms', '0010_alter_cameraconfigurationfile_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysisresult',
            name='filename',
            field=models.FileField(unique=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='datain',
            name='filename',
            field=models.FileField(unique=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='photo',
            name='filename',
            field=models.FileField(unique=True, upload_to=''),
        ),
    ]
