# Generated by Django 5.1.3 on 2024-11-28 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='truck',
            name='cuisine',
            field=models.CharField(choices=[('MEX', 'Mexican'), ('ITA', 'Italian'), ('JPN', 'Japanese'), ('IND', 'Indian'), ('CHI', 'Chinese'), ('VGT', 'Vegetarian')], max_length=3),
        ),
    ]
