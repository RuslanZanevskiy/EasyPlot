# Generated by Django 5.0.2 on 2024-08-10 11:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plots", "0003_like"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plot",
            name="description",
            field=models.TextField(),
        ),
    ]
