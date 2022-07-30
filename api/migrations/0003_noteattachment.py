# Generated by Django 4.0.6 on 2022-07-30 15:03

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_note_attachments'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, null=True, upload_to=api.models.upload_to)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noteattachment', to='api.note')),
            ],
        ),
    ]