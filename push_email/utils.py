__author__ = 'hannon'

import threading
import re
from email.utils import parsedate_to_datetime

from imbox import Imbox

from .models import MyEmail, EmailId



# Global Variables
pattern = re.compile('\[BCC423\]\[\d{2}\.\d\.\d{4}] Agenda \d{2}/\d{2}/\d{4} \d{2}:\d{2}')
timeout = 60

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
    """
    Saves a given email in the database
    :param message: email message
    :return:
    """
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
    """
    Formats an even to add it to google calendar
    :param message: an email message
    :return:
    """

    # event_date_time = re.search('\d{2}/\d{2}/\d{4} \d{2}:\d{2}', message.subject).group()  # gets the event date and time as str
    # local = pytz.timezone("America/Sao_Paulo") # gets SP time
    # naive_date = datetime.datetime.strptime(event_date_time, "%d/%m/%Y %H:%M")  # converts str to a naive datetime
    # aware_date = naive_date.replace(tzinfo=local) # converts into an aware date type
    #
    # str_formated_date = aware_date.isoformat()
    #
    # event = {
    #     'description': 'BCC432 - Agenda',
    #     'start': {
    #         'dateTime': str_formated_date,
    #         'timeZone': local,
    #     },
    #     'end': {
    #         'dateTime': aware_date + datetime.timedelta(hours=1),
    #         'timeZone': local,
    #     }
    # }

    event = {
      'start': {
        'dateTime': '2015-05-28T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '2015-05-28T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
    }




def load_already_seen():
    """
    Loads messages that have already been seen in previous runs of this
    code so that they don't appear as duplicate in the view for the user
    :return:
    """
    seen = EmailId.objects.all()
    print("Number of already seen emails ", seen.count())
    if seen:
        for s in seen:
            already_seen.add(s.email_id)


class EmailThread(threading.Thread):

    def __init__(self, username, password, imap_id):
        """
        EmailThread constructor.
        :param username: username to log in the email account
        :param password: password for the given account
        :param imap_id: an ID to identify which imap code to use: 1 = gmail, 2 = yahoo
        """
        threading.Thread.__init__(self)

        self.username = username
        self.password = password
        self.imap_id = imap_id

    def run(self):
        """
        Runs this thread
        """

        print("Starting thread ", self.username)
        print()
        self.imbox = login(self.username, self.password, self.imap_id)

        #load_already_seen()
        self.check_for_new_emails()

    def check_for_new_emails(self):
        """
        Checks for new emails that match the pattern "[BBC423][xx.x.xxxx] Agenda dd/mm/aaaa hh:mm"
        """
        print("Checking for new emails on ", self.username)
        sleep_for = threading.Event()

        while True:
            unread_messages = self.imbox.messages()

            for uid, message in unread_messages:
                if  pattern.match(message.subject) and message.message_id not in already_seen:
                    EmailId.objects.create(
                        email_id=message.message_id
                    )
                    already_seen.add(message.message_id)  # workaround to avoid repeated emails

                    print("Subject: ", message.subject)
                    save_email(message)
                    #add_to_calendar(message)

        print("%s is going to sleep for %d seconds"%(self.username, timeout))
        sleep_for.wait(timeout=timeout) # sleeps for n seconds
        print("%s is waking up"%(self.username))

