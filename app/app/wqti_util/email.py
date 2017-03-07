import logging
from django.conf import settings
from django.core.mail import EmailMessage as DjangoEmailMessage
from django.template import loader, Context


class EmailMessage(object):
    def __init__(self, to, subject, template, context, from_email=None, bcc=[]):
        '''  
        If "from" is None, then use settings.DEFAULT_FROM_EMAIL
        '''
        self.to = [to] if not (isinstance(to, list) or isinstance(to, tuple)) else to
        self.bcc = [bcc] if not (isinstance(bcc, list) or isinstance(bcc, tuple)) else bcc
        self.subject = subject
        self.template = template
        self.context = context
        self.from_email = from_email or settings.DEFAULT_FROM_EMAIL 
        logging.debug('to: %s, bcc: %s, subject: %s, from_email: %s' % (self.to, self.bcc, self.subject, self.from_email))
    
    def send(self):
        ''' 
        Returns True/False
        '''
        t = loader.get_template(self.template)
        msg = DjangoEmailMessage(self.subject, t.render(Context(self.context)), 
                            self.from_email, self.to, self.bcc)
        
        try:
            msg.send(fail_silently=False)
        except Exception, e:
            logging.debug('%s' % e)
            return False
        return True