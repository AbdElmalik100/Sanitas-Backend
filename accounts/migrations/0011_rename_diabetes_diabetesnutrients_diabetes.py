# Generated by Django 4.2.9 on 2024-07-01 21:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_rename_added_sugars_diabetesnutrients_diabetes_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diabetesnutrients',
            old_name='Diabetes',
            new_name='diabetes',
        ),
    ]
