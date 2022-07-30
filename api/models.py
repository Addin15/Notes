from distutils.command.upload import upload
from django.db import models
from django.contrib.postgres.fields import ArrayField
import os


def upload_to(instance, filename):
    return os.path.join('attachments/' + str(instance.note.user) + '/' + str(instance.note.pk) + '/' + filename)


class Note(models.Model):
    user = models.TextField()
    text = models.TextField()

    def __str__(self):
        return self.name


class NoteAttachment(models.Model):
    note = models.ForeignKey(Note,
                             related_name="noteattachment", on_delete=models.CASCADE)  # NOQA
    attachment = models.FileField(upload_to=upload_to,
                                  null=True, blank=True)
