from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext
from .utils import EmailThread
from .models import MyEmail
from time import sleep
from django.views.generic.edit import FormView
from .forms import LoginForm


class FullEmail:
    def __init__(self, email_subject=None, email_from=None, email_body=None, email_date=None, recipients=None, copies=None):
        self.email_subject = email_subject
        self.email_from = email_from
        self.email_body = email_body
        self.email_date = email_date
        self.recipients = []
        self.copies = []


class EmailLoginView(FormView):
    template_name = 'index.html'
    form_class = LoginForm
    success_url = '/home/'


class EmailView(View):
    template_name = 'emails.html'

    def post(self, request):

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


