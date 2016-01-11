__author__ = 'hannon'

from imbox import Imbox
import threading
import re

pattern = re.compile('\[BCC264\]\[\d{2}\.\d\.\d{4}] Agenda \d{2}/\d{2}/\d{4}')

imap = {1: 'imap.gmail.com',
        2: 'imap.mail.yahoo.com'}


def login(username, password, imap_id):

    """
    Tries to log in and return the imbox object
    :param username:
    :param password:
    :param imap_id:
    :return: imbox
    """

    try:
        imbox = Imbox(
                imap[imap_id],
                username=username,
                password=password,
                ssl=True
            )
        print("%s is logged in"%(username))
    except:
        print("Login failed")
        return None

    return imbox


def save_email(message):
    pass

def add_to_calendar(message):
    pass

class EmailThread(threading.Thread):
    def __init__(self, username, password, imap_id):
        print("Thread for ", username)
        threading.Thread.__init__(self)

        self.username = username
        self.password = password
        self.imap_id = imap_id

        #self.imbox = login(username, self.password, self.imap_id)

    def run(self):
        print("Starting thread ", self.username)
        print()
        self.imbox = login(self.username, self.password, self.imap_id)
        self.check_for_new_emails()

    def check_for_new_emails(self):
        print("Checking for new emails on ", self.username)
        sleep_for = threading.Event()

        while True:
            unread_messages = self.imbox.messages()

            for uid, message in unread_messages:
                if pattern.match(message.subject):
                    print("Subject: ", message.subjetc)
                    save_email(message)
                    add_to_calendar(message)

            print("Going to sleep")
            sleep_for.wait(timeout=30) # sleeps for 60 seconds
            print("Woke up")



t1 = EmailThread('bcc264decom@gmail.com', 'bcc264bcc264', 1)
t2 = EmailThread('bcc264decom@yahoo.com', 'bcc264bcc264', 2)

t1.start()
t2.start()

print("Exiting main thread")
