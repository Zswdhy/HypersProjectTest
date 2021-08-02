# Generated by Django 3.2.5 on 2021-07-30 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('e_name', models.CharField(max_length=64)),
                ('e_age', models.IntegerField()),
                ('e_job', models.CharField(blank=True, max_length=64, null=True)),
                ('province', models.CharField(blank=True, max_length=32, null=True)),
                ('city', models.CharField(blank=True, max_length=32, null=True)),
                ('p_name', models.CharField(max_length=64)),
                ('join_time', models.DateTimeField(auto_now=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'employee',
            },
        ),
    ]