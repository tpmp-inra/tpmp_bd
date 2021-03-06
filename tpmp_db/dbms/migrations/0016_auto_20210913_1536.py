# Generated by Django 3.2.7 on 2021-09-13 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbms', '0015_auto_20210913_1456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annotation',
            name='label',
        ),
        migrations.AlterField(
            model_name='annotation',
            name='level',
            field=models.CharField(choices=[('DEBUG', 'DEBUG'), ('INFO', 'INFO'), ('WARNING', 'WARNING'), ('ERROR', 'ERROR'), ('CRITICAL', 'CRITICAL')], max_length=30),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='state',
            field=models.CharField(choices=[('DEBUG', 'DEBUG'), ('INFO', 'INFO'), ('WARNING', 'WARNING'), ('ERROR', 'ERROR'), ('CRITICAL', 'CRITICAL')], max_length=30),
        ),
    ]
