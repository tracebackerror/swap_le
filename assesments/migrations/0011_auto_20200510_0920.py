# Generated by Django 3.0.5 on 2020-05-10 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assesments', '0010_auto_20200509_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.TextField(),
        ),
    ]
