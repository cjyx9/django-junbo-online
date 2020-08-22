# Generated by Django 3.1 on 2020-08-21 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=128, unique=True)),
                ('realName', models.CharField(max_length=128, unique=True)),
                ('anoahName', models.CharField(max_length=128, unique=True)),
                ('aeduName', models.CharField(max_length=128, unique=True)),
                ('aeduPassword', models.CharField(max_length=128, unique=True)),
                ('passWord', models.CharField(max_length=256)),
                ('signinTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['signinTime'],
            },
        ),
    ]