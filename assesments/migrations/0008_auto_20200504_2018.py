# Generated by Django 3.0.5 on 2020-05-04 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assesments', '0007_auto_20200504_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='publish_result',
            field=models.BooleanField(default=True),
        ),
    ]