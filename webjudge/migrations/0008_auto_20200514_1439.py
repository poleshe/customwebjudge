# Generated by Django 2.2.12 on 2020-05-14 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webjudge', '0007_remove_test_steps_step_action'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test_steps',
            old_name='user_id',
            new_name='test_name',
        ),
    ]