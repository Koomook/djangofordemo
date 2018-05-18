# Generated by Django 2.0.5 on 2018-05-18 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lyrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('extention', models.CharField(default='html', max_length=10)),
                ('lyrics', models.TextField()),
                ('outputs', models.TextField()),
                ('keyword', models.TextField()),
                ('inputs', models.TextField()),
                ('inputs_idx', models.TextField()),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('song', models.TextField()),
                ('extention', models.CharField(default='mp3', max_length=10)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
