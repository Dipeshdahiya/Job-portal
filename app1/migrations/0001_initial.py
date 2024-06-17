# Generated by Django 5.0.4 on 2024-05-12 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('job_title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('responsibilities', models.TextField()),
                ('skills_needed', models.TextField()),
                ('salary', models.CharField(max_length=50)),
                ('date_added', models.DateField()),
                ('contact_information', models.CharField(max_length=255)),
            ],
        ),
    ]