# Generated by Django 5.0.2 on 2024-02-14 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_vote"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vote",
            old_name="owner",
            new_name="voter",
        ),
    ]
