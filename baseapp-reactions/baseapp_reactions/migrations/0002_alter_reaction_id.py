# Generated by Django 3.2 on 2023-08-21 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("baseapp_reactions", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reaction",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
