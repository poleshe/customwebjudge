# Generated by Django 2.2.12 on 2020-05-24 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webjudge', '0005_users_tests_resolved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='surname',
            field=models.CharField(max_length=1500),
        ),
    ]
