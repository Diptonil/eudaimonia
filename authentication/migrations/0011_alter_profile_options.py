# Generated by Django 3.2.12 on 2022-03-29 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_alter_profile_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('join_date',)},
        ),
    ]
