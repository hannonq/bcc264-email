from imbox import Imbox


'''imap.gmail.com'''
imbox = Imbox('imap.mail.yahoo.com',
              username='bcc264decom@yahoo.com', 
              password='bcc264bcc264',
              ssl=True)

unread_messages = imbox.messages(unread=True)

for uid, message in unread_messages:
    print("Sent from ", message.sent_from)
    print("Subject ", message.subject)
    print("Body ", message.body.get('plain'))
