# Generated by Django 3.2 on 2021-05-07 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('section', models.PositiveIntegerField(choices=[(1, 'Codigo'), (2, 'Diseño'), (3, 'Blockchain'), (4, 'Emprendimiento')])),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('assets', models.BinaryField()),
                ('summary', models.CharField(max_length=500)),
                ('datetime', models.DateTimeField()),
                ('upvotes', models.IntegerField()),
                ('downvotes', models.IntegerField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'unique_together': {('post_id', 'user_id')},
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('datetime', models.DateTimeField()),
                ('upvotes', models.IntegerField()),
                ('downvotes', models.IntegerField()),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'unique_together': {('comment_id', 'post_id', 'user_id')},
            },
        ),
    ]