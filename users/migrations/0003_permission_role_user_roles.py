# Generated by Django 4.2.11 on 2024-03-15 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_groups_user_is_active_user_is_staff_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('permission_id', models.AutoField(primary_key=True, serialize=False)),
                ('permission_name', models.CharField()),
            ],
            options={
                'db_table': 'Permissions',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.AutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=50)),
                ('permissions', models.ManyToManyField(related_name='roles', to='users.permission')),
            ],
            options={
                'db_table': 'Roles',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(related_name='users', to='users.role'),
        ),
    ]
