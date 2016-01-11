from django.db import models


class Recipient(models.Model):
    email_to = models.EmailField(null=False)
    email = models.ForeignKey('MyEmail', on_delete=models.CASCADE) # one email can one or more recipients

class Copy(models.Model):
    copy_to = models.EmailField(null=True)
    email = models.ForeignKey('MyEmail', on_delete=models.CASCADE) # one email can have zero or more CC

class MyEmail(models.Model):
    email_subject = models.CharField(null=True, max_length=255)
    email_from = models.EmailField()
    email_body = models.TextField(null=True)
