# Generated by Django 3.1 on 2020-08-22 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='UserSelf',
        ),
        migrations.AlterModelOptions(
            name='userself',
            options={'ordering': ['signinTime'], 'verbose_name': '用户_外部', 'verbose_name_plural': '用户_外部'},
        ),
    ]
