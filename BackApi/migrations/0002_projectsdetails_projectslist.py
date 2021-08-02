# Generated by Django 3.2.5 on 2021-08-02 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BackApi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectsList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('p_name', models.CharField(max_length=64)),
                ('p_start_time', models.DateField(blank=True, null=True)),
                ('p_end_time', models.DateField(blank=True, null=True)),
                ('employee_num', models.IntegerField(blank=True, null=True)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'project_list',
            },
        ),
        migrations.CreateModel(
            name='ProjectsDetails',
            fields=[
                ('pd_id', models.IntegerField(primary_key=True, serialize=False)),
                ('p_name', models.CharField(max_length=64)),
                ('p_introduce', models.CharField(max_length=255)),
                ('e_name', models.CharField(max_length=32)),
                ('e_age', models.IntegerField(blank=True, null=True)),
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BackApi.projectslist')),
            ],
            options={
                'db_table': 'project_details',
            },
        ),
    ]
