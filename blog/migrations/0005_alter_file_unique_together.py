# Generated by Django 3.2 on 2021-07-03 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_file_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='file',
            unique_together=set(),
        ),
    ]