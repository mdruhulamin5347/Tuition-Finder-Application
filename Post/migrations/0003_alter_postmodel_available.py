# Generated by Django 4.2.2 on 2024-08-20 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0002_alter_postmodel_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='available',
            field=models.BooleanField(default=False),
        ),
    ]
