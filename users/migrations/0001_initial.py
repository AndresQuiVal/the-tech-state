# Generated by Django 3.2 on 2021-05-07 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=50)),
                ('profile_img', models.CharField(max_length=150)),
            ],
        ),
    ]
