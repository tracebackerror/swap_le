# Generated by Django 3.0.5 on 2020-04-25 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='parent_contact_no',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_contact_no',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
