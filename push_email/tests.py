from django.test import TestCase

from .models import Recipient, Copy, MyEmail
from .utils import EmailThread

class EmailTestCase(TestCase):
    def test_email_creation(self):
        r1 = Recipient.objects.create(email_address='recipient1@gmail.com')
        r2 = Recipient.objects.create(email_address='recipient2@gmail.com')
        email1 = MyEmail(
            email_subject='subject of email1',
            email_from='tester@gmail.com',
            email_body='Body of the first email',
        )
        email1.save()
        email1.recipients.add(r1, r2)

        print(email1.recipients.all())


class ThreadTestCase(TestCase):
    def test_thread(self):
        t1 = EmailThread('bcc264decom@gmail.com', 'bcc264bcc264', 1)
        t2 = EmailThread('bcc264decom@yahoo.com', 'bcc264bcc264', 2)

        t1.start()
        t2.start()


