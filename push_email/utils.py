__author__ = 'hannon'

from imbox import Imbox
from .models import MyEmail, Copy, Recipient
import threading
import re
from email.utils import parsedate_to_datetime


#Global Variables
pattern = re.compile('\[BCC423\]\[\d{2}\.\d\.\d{4}] Agenda \d{2}/\d{2}/\d{4}')
timeout = 10

imap = {1: 'imap.gmail.com',
        2: 'imap.mail.yahoo.com'}

already_seen = set()


def login(username, password, imap_id):

    """
    Tries to log in and return the imbox object
    :param username:
    :param password:
    :param imap_id:
    :return: imbox
    """
    print("Trying to log in with ", username)
    try:
        imbox = Imbox(
                imap[imap_id],
                username=username,
                password=password,
                ssl=True
            )
        print("%s is logged in\n"%(username))
    except:
        print("Login failed")
        return None

    return imbox


def save_email(message):
    ccs = message.cc
    recipients = message.sent_to

    parsed_date = parsedate_to_datetime(message.date)

    email = MyEmail(
        email_subject=message.subject,
        email_from=message.sent_from[0].get('email'),
        email_body=message.body.get('plain'),
        date=parsed_date
    )

    email.save()
    if ccs:
        for cc in ccs:
            email.copies.create(email_address=cc.get('email'))

    for r in recipients:
        email.recipients.create(email_address=r.get('email'))

def add_to_calendar(message):
    pass

class EmailThread(threading.Thread):
    def __init__(self, username, password, imap_id):
        threading.Thread.__init__(self)

        self.username = username
        self.password = password
        self.imap_id = imap_id


    def run(self):
        print("Starting thread ", self.username)
        print()
        self.imbox = login(self.username, self.password, self.imap_id)
        self.check_for_new_emails()

    def check_for_new_emails(self):
        """
        Checks for new emails that match the pattern
        :return:
        """
        print("Checking for new emails on ", self.username)
        sleep_for = threading.Event()

        while True:
            unread_messages = self.imbox.messages()

            for uid, message in unread_messages:
                if pattern.match(message.subject) and message.message_id not in already_seen:
                    already_seen.add(message.message_id) # workaround to avoid repeated emails

                    print("Subject: ", message.subject)
                    save_email(message)
                    add_to_calendar(message)

            print("%s is going to sleep for %d seconds"%(self.username, timeout))
            sleep_for.wait(timeout=timeout) # sleeps for n seconds
            print("%s is waking up"%(self.username))

#
#
# t1 = EmailThread('bcc264decom@gmail.com', 'bcc264bcc264', 1)
# t2 = EmailThread('bcc264decom@yahoo.com', 'bcc264bcc264', 2)
#
# t1.start()
# t2.start()
#
# print("Exiting main thread")
