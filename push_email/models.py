import datetime

from django.db import models


class Copy(models.Model):
    """
    Creates a "copy" table
    """
    email_address = models.EmailField(null=True)

    def __str__(self):
        return "CC: " + self.email_address

class Recipient(models.Model):
    """
    Creates a "recipient" table
    """
    email_address = models.EmailField(null=False, blank=False)

    def __str__(self):
        return "to: " + self.email_address


class MyEmail(models.Model):
    """
    Email object to save all useful email information
    """
    recipients = models.ManyToManyField('Recipient')
    copies = models.ManyToManyField('Copy')

    email_subject = models.CharField(null=True, max_length=255)
    email_from = models.EmailField()
    email_body = models.TextField(null=True)
    date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return 'Subject: ' + self.email_subject + '\n' + 'From: ' + self.email_from


class EmailId(models.Model):
    """
    A unique email ID
    """

    email_id = models.TextField()


