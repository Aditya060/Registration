# Generated by Django 4.2.16 on 2024-09-08 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_user_gender_remove_user_venue_user_company_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
