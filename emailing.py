import smtplib
import imghdr
from email.message import EmailMessage

PASSWORD = 'ijphifxzeesvcipt'
SENDER = 'rbn.leona@gmail.com'
RECEIVER = 'rbn.leona@gmail.com'

def send_email(img_path):
    email_message = EmailMessage()
    email_message['Subject'] = 'New customer'
    email_message.set_content('New customer showed up on camera')

    with open(img_path, 'rb') as file:
        content = file.read()
    email_message.add_attachment(content, maintype='image',
                                 subtitle=imghdr.what(None, content))
    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER,PASSWORD)
    gmail.sendmail(SENDER,RECEIVER, email_message.as_string())
    gmail.quit()

if __name__ == '__main__':
    send_email(img_path='images/')

