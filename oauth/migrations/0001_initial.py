# Generated by Django 3.1.2 on 2020-10-25 00:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('can_delete', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'oauth_group',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=512)),
                ('description', models.CharField(max_length=128)),
                ('permissionArea', models.CharField(max_length=128)),
                ('needPermission', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'oauth_permission',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=254, null=True, unique=True)),
                ('name', models.CharField(max_length=512)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('image', models.FileField(upload_to='user_avatar')),
                ('birth_date', models.DateField(null=True)),
                ('last_login', models.DateTimeField(null=True)),
                ('need_logout', models.BooleanField(default=False)),
                ('news_letter', models.IntegerField(default=None, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'oauth_user',
            },
        ),
        migrations.CreateModel(
            name='UserPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='oauth.permission')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oauth.user')),
            ],
            options={
                'db_table': 'oauth_user_permission',
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='oauth.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oauth.user')),
            ],
            options={
                'db_table': 'oauth_user_group',
            },
        ),
        migrations.CreateModel(
            name='GroupPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oauth.group')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='oauth.permission')),
            ],
            options={
                'db_table': 'oauth_group_permission',
            },
        ),
    ]
