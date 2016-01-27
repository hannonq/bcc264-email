from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.edit import FormView

from .utils import EmailThread
from .models import MyEmail
from .forms import LoginForm


class FullEmail:
    """
    Creates a new Email object with all fields that will be used in the html templates
    """
    def __init__(self, email_subject=None, email_from=None, email_body=None, email_date=None, recipients=None, copies=None):
        """
        Constructor for a new FullEmail object
        :param email_subject: Subject of the message
        :param email_from: Sender of the email
        :param email_body: Body of the email
        :param email_date: Date when the email was sent
        :param recipients: List of recipients for this email
        :param copies: List of email to whom this email will be copied
        :return: None
        """
        self.email_subject = email_subject
        self.email_from = email_from
        self.email_body = email_body
        self.email_date = email_date
        self.recipients = []
        self.copies = []


class EmailLoginView(FormView):
    """
    Renders the login view
    """
    template_name = 'index.html'
    form_class = LoginForm
    success_url = '/home/'


class EmailView(View):
    """
    Renders the email view page
    """
    template_name = 'emails.html'

    def post(self, request):
        """
        Gets a POST request with the login data and sends it to the backend
        :param request: POST request from the Login view
        :return: None
        """

        gmail_address = request.POST['email_address1']
        gmail_pwd = request.POST['password1']

        yahoo_address = request.POST['email_address2']
        yahoo_pwd = request.POST['password2']

        t1 = EmailThread(gmail_address, gmail_pwd, 1)
        t2 = EmailThread(yahoo_address, yahoo_pwd, 2)

        t1.start()
        t2.start()
        #sleep(2)

        email_list = []
        for e in MyEmail.objects.all():
            recipients_list = []
            copies_list = []

            for r in e.recipients.all():
                recipients_list.append(r)

            for c in e.copies.all():
                copies_list.append(c)

            new_email = FullEmail(
                e.email_subject,
                e.email_from,
                e.email_body,
                e.date,
                recipients_list,
                copies_list
            )
            email_list.append(new_email)

        context = {'emails': email_list}

        return render_to_response(self.template_name, context, context_instance=RequestContext(request))


