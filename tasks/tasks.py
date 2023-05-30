import smtplib
from email.message import EmailMessage

from fastapi import Body

from config import SMTP_PASSWORD, SMTP_USER
from schemas.users import UserSchema

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def get_email_template(payload: UserSchema = Body()):
    email = EmailMessage()
    email['Subject'] = 'Вы успешно зарегистрировались'
    email['From'] = SMTP_USER
    email['To'] = payload.email

    email.set_content(
        '<div>'
        f'<h1 style="color: Black;">Вы успешно зарегистрировались на сайте http://81.200.145.113:8000/pages/main_page .</h1>'
        '<img src="https://i.pinimg.com/564x/06/0a/90/060a90c03ea5e7012d6cc9beb344488a.jpg" alt="тут была картинка">'

        # '-management-dashboard-ui-design-template-suitable-designing-application-for-android-and-ios-clean-style-app'
        # '-mobile-free-vector.jpg" width="600">'
        '</div>',
        subtype='html'
    )
    return email


def send_email(username: str):
    email = get_email_template(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)