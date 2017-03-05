import os
import sendgrid


class Mail:
    def __init__(self, to, subject, msg):
        self.to = to
        self.subject = subject
        self.msg = msg

    def send(self):
        sg = sendgrid.SendGridClient(os.environ.get('SENDGRID_KEY', ''))
        message = sendgrid.Mail()
        message.add_to(self.to)
        print self.to
        message.set_subject(self.subject)
        print self.subject
        message.set_html(self.msg)
        message.set_text(self.msg)
        print self.msg
        message.set_from('cx-col <encuestas@cx-col.com>')
        print (sg.send(message))