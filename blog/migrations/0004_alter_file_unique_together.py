# Generated by Django 3.2 on 2021-07-03 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210703_1158'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='file',
            unique_together={('id', 'post')},
        ),
    ]
