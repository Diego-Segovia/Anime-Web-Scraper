import smtplib
from email.mime.text import MIMEText

app_email = "WeebScraper@gmail.com"
app_password = "chnqsdhbejgcptyk"

all_user_emails = [app_email]


class Email:
    smtp_object = None

    def __init__(self):
        self.smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp_object.ehlo()
        self.smtp_object.starttls()
        self.smtp_object.login(app_email, app_password)

    def format_mail(self, anime_name, anime_link):
        email_body = """<pre> 
""" + anime_name + """ New Episode:
<form action = """ + """ " """ + anime_link + """ " """ + """>
<button type = "submit" style= "background-color: #676767"> Watch New Episode!</button>
</form>
Thank you for using,
WeebScraper.
</pre>"""

        formatted_body = MIMEText(email_body, 'html')

        msg = "Subject: " + anime_name + " NEW EPISODE!" + '\n' + formatted_body.as_string()

        return msg

    def send_mail(self, msg):
        self.smtp_object.sendmail(app_email, all_user_emails, msg)

    def add_email(self, email):
        all_user_emails.append(email)
