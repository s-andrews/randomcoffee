#!/usr/bin/python3
import cgi
import smtplib
from email.message import EmailMessage

def main():
    form = cgi.FieldStorage()
    action = form.getvalue("action").strip()

    if action == "signup":
        subscribe(form.getvalue("name"),form.getvalue("email"))

    else:
        print (f"Status: 500 Bad Action {action}\nContent-type: text/html\n")

def subscribe(name,email):

    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content("You've signed up for a random coffee.  To prove it really was you please click on the link below to confirm your signup.")

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = f'Random Coffee Trial Signup'
    msg['From'] = "Simon Andrews <simon.andrews@babraham.ac.uk>"
    msg['To'] = (f"{name} <{email}>")

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

    print(f"Content-type: text/plain\n")
    print(f"Action was sent email")


if __name__ == "__main__":
    main()