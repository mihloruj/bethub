# Generated by Django 3.1.4 on 2021-02-01 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210201_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nextmatch',
            name='old',
            field=models.BooleanField(default=False),
        ),
    ]
