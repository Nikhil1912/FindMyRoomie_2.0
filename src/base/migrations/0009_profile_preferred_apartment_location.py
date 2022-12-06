# Generated by Django 4.1.1 on 2022-12-05 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_profile_apartment_photo_profile_city_profile_drug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='preferred_apartment_location',
            field=models.CharField(blank=True, choices=[('Raleigh', 'Raleigh'), ('Durham', 'Durham'), ('Cary', 'Cary'), ('Other', 'Other')], max_length=128),
        ),
    ]