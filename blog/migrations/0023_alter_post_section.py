# Generated by Django 3.2.5 on 2021-11-27 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_remove_post_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='section',
            field=models.CharField(choices=[('code', 'Code'), ('design', 'Design'), ('blockchain', 'Blockchain'), ('entrepreneurship', 'Entrepreneurship')], max_length=50),
        ),
    ]
