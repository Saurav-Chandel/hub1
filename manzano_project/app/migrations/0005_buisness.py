# Generated by Django 4.0.2 on 2022-02-04 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_report_user_report_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buisness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='buisness_image')),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
