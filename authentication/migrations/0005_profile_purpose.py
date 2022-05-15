# Generated by Django 4.0.3 on 2022-03-09 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='purpose',
            field=models.CharField(choices=[('Personal', 'Personal'), ('Travelogue', 'Travelogue'), ('Cookbook', 'Cookbook'), ('Spiritual', 'Spiritual'), ('Daily Log', 'Daily Log')], default='Personal', max_length=16),
        ),
    ]
