# Generated by Django 4.2.4 on 2023-09-01 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_documents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='document_size',
            field=models.PositiveIntegerField(),
        ),
    ]
