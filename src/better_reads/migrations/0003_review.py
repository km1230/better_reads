# Generated by Django 2.2.11 on 2021-01-13 04:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("better_reads", "0002_shelf"),
    ]

    operations = [
        migrations.RenameModel(old_name="Note", new_name="Review",),
    ]