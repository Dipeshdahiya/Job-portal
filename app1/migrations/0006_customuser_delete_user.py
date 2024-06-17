# Generated by Django 5.0.4 on 2024-06-09 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_user_remove_joblisting_contact_information_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
