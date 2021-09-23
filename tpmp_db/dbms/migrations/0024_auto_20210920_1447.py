# Generated by Django 3.2.7 on 2021-09-20 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dbms', '0023_annotation_target_class_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('website', models.CharField(max_length=520)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterModelOptions(
            name='analysisresult',
            options={'ordering': ['filename']},
        ),
        migrations.AlterModelOptions(
            name='annotation',
            options={'ordering': ['timestamp']},
        ),
        migrations.AlterModelOptions(
            name='cameraconfigurationfile',
            options={'ordering': ['filename']},
        ),
        migrations.AlterModelOptions(
            name='datain',
            options={'ordering': ['timestamp']},
        ),
        migrations.AlterModelOptions(
            name='experiment',
            options={'ordering': ['date_start']},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ['label']},
        ),
        migrations.AlterModelOptions(
            name='measure',
            options={'ordering': ['label']},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['user']},
        ),
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['filename']},
        ),
        migrations.AlterModelOptions(
            name='plant',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='sensor',
            options={'ordering': ['label']},
        ),
        migrations.AlterModelOptions(
            name='weighting',
            options={'ordering': ['label']},
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='allowed_persons',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='interaction',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='researcher',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='species',
        ),
        migrations.RemoveField(
            model_name='person',
            name='affiliation',
        ),
        migrations.RemoveField(
            model_name='person',
            name='mail',
        ),
        migrations.RemoveField(
            model_name='person',
            name='name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='surname',
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('species', models.CharField(blank=True, max_length=30, null=True)),
                ('interaction', models.CharField(blank=True, max_length=30, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dbms.organization')),
                ('participants', models.ManyToManyField(blank=True, null=True, related_name='person_experience', to='dbms.Person')),
                ('researcher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='researcher', to='dbms.person')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='experiment',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dbms.project'),
        ),
        migrations.AddField(
            model_name='person',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dbms.organization'),
        ),
    ]
