#!/usr/bin/python3
import cgi
import smtplib
from email.message import EmailMessage
import sqlite3
import random
import string


conn = sqlite3.connect("db/rct.db")
base_url = "https://www.bioinformatics.babraham.ac.uk/rct/rct.py"

# Only run this to establish the db to start with.
# c = conn.cursor()
# c.execute('CREATE TABLE person (name text, email text)')
# c.execute('CREATE TABLE request (action, text, name text, email text, secret text)')
# conn.commit()


def main():
    form = cgi.FieldStorage()
    action = form.getvalue("action").strip()

    if action == "signup":
        subscribe(form.getvalue("name"),form.getvalue("email"))

    else:
        print (f"Status: 500 Bad Action {action}\nContent-type: text/html\n")

def subscribe(name,email):

    # Get a random code
    code = random_code()

    # Add an entry to the database
    c = conn.cursor()

    c.execute("INSERT INTO request (action,name,email,secret) values (?,?,?,?)",("subscribe",name,email,code))

    conn.commit()

    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(f"You've signed up for a random coffee.  To prove it really was you please click on the link below to confirm your signup.\n\n{base_url}?action=validate&code={code}\n\nIf it wasn't you please delete this message and move on with your life :-)")

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


def random_code():
    code = []

    for _ in range(20):
        code.append(random.choice(string.ascii_letters + string.digits))

    return "".join(code)


if __name__ == "__main__":
    main()