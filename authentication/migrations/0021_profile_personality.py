# Generated by Django 3.2.13 on 2022-06-29 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0020_delete_frequencystatistics'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='personality',
            field=models.CharField(default=None, max_length=4, null=True),
        ),
    ]