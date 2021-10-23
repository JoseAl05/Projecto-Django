import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app import settings
from django.template.loader import render_to_string


def send_email():
    try:
        mailServer = smtplib.SMTP(settings.EMAIL_HOST,settings.EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
        print('CONECTADO')

        email_to = 'deserrapqta@gmail.com'

        msj = MIMEMultipart()
        msj['From'] = settings.EMAIL_HOST_USER
        msj['To'] = email_to
        msj['Subject'] = 'Correo de prueba DJANGO'

        content = render_to_string('email.html')
        msj.attach(MIMEText(content,'html'))

        mailServer.sendmail(settings.EMAIL_HOST_USER,email_to,msj.as_string())

        print('Correo Enviado Correctamente')
    except Exception as e:
        print(e)

send_email()
