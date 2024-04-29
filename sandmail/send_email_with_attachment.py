import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email_with_attachment(send_from, send_to, subject, body, files, server, port, username, password):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    for f in files:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=f
            )
        part['Content-Disposition'] = f'attachment; filename="{f}"'
        msg.attach(part)

    with smtplib.SMTP_SSL(server, port) as server:
        server.login(username, password)
        server.send_message(msg)
