# Generated by Django 3.2.13 on 2022-06-13 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_auto_20220614_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favmusicfield',
            name='field',
            field=models.CharField(default='All', max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='unfavmoviefield',
            name='field',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='unfavmusicfield',
            name='field',
            field=models.CharField(max_length=16, null=True),
        ),
    ]