# Generated by Django 4.1.6 on 2023-02-13 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rendez_vous', '0006_alter_note_content_alter_note_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='user',
            new_name='client',
        ),
    ]
