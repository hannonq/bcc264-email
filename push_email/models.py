import datetime

from django.db import models


class Copy(models.Model):
    email_address = models.EmailField(null=True)

    def __str__(self):
        return "CC: " + self.email_address

class Recipient(models.Model):
    email_address = models.EmailField(null=False, blank=False)

    def __str__(self):
        return "to: " + self.email_address


class MyEmail(models.Model):
    recipients = models.ManyToManyField('Recipient')
    copies = models.ManyToManyField('Copy')

    email_subject = models.CharField(null=True, max_length=255)
    email_from = models.EmailField()
    email_body = models.TextField(null=True)
    date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return 'Subject: ' + self.email_subject + '\n' + 'From: ' + self.email_from


class EmailId(models.Model):

    email_id = models.TextField()


