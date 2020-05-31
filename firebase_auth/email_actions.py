import os
import concurrent.futures
import smtplib
import time
from email.message import EmailMessage

def send_msg(to_addr):
    msg = EmailMessage()
    msg['Subject']='Grab dinner this weekend?'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_addr
    msg.set_content('How about dinnner at 6pm this saturday new')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        # Login to email
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        # Send message
        smtp.send_message(msg)

class Email:
    def __init__(self):
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 465

    def generate_email_verification_message(self, recipient_name, recipient_email, verification_link):
        content = f"Hello {recipient_name},\nFollow this link to verify your email address.\n{verification_link}\nIf you didn't ask to verify this address, you can ignore this email.\n Thanks,\nYour Flask-Snipets team"
        msg = EmailMessage()
        msg['Subject'] = f'{recipient_name}, Please Verify Your Email Address.'
        msg['From'] = 'noreply@flask-snippets.firebaseapp.com'
        msg['To'] = recipient_email
        msg.set_content(content)

        return msg

    def generate_welcome_message(self, recipient):
        pass

    def generate_password_reset(self, recipient, varification_link):
        pass
    
    def send_async_email(self, msg):
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as smtp:
            smtp.login(os.environ.get('GMAIL_ADDRESS'), os.environ.get('GMAIL_APP_PASSWORD'))
            smtp.send_message(msg)
            

    def send_email(self, msg):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.send_async_email, msg)

def do_something(seconds):
    print(f'sleeping {seconds} seconds')
    time.sleep(seconds)
    return 'done sleeping ...'

def async_process(func, *args):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(func, *args)
        print(f1.result())
    print('out')
            
        
    

    
