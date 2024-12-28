import smtplib
# Gives metadata about images
import imghdr
from email.message import EmailMessage
import os

PASSWORD = os.getenv("PASSWORD")
SENDER = os.getenv("EMAIL")
RECEIVER = os.getenv("EMAIL2")


def send_email(image_obj):
    email_message = EmailMessage()
    email_message["Subject"] = "Customer!"
    email_message.set_content("We got you a customer waiting!")

    with open(image_obj, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP_SSL("smtp.gmail.com", port=587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(RECEIVER, PASSWORD, email_message.as_string())
    gmail.quit()
