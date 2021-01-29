#!/usr/bin/python3
import cgi
import smtplib
from email.message import EmailMessage
import sqlite3
import random
import string
import sys


conn = sqlite3.connect("db/rct.db")

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
    elif action == "unsubscribe":
        unsubscribe(form.getvalue("email"))
    elif action == "validate":
        validate(form.getvalue("code"))

    else:
        send_error (f"Bad Action {action}")

def send_error(error):
        print (f"Status: 500 Error {error}\nContent-type: text/html\n")


def subscribe(name,email):

    # Get a random code
    code = random_code()

    # Add an entry to the database
    c = conn.cursor()

    c.execute("INSERT INTO request (action,name,email,secret) values (?,?,?,?)",("subscribe",name,email,code))

    conn.commit()

    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(f"You've signed up for a random coffee.  To prove it really was you please enter the code below into the validation form.\n\nYour code is {code}\n\nIf it wasn't you please delete this message and move on with your life :-)")

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


def unsubscribe(email):

    # Make a connection
    c = conn.cursor()

    # Delete any previous requests from this person
    c.execute("DELETE FROM request WHERE email=?",(email,))

    # check to see if this email is subscribed.  If they're not then give up
    c.execute("SELECT name,email FROM person WHERE email=?",(email,))

    existing = c.fetchall()

    print("Email was "+email, file=sys.stderr)

    if not existing:
        # They're not subscribed
        send_error("Not subscribed")
        return

    name = existing[0][0]

    # Get a random code
    code = random_code()

    c.execute("INSERT INTO request (action,name,email,secret) values (?,?,?,?)",("unsubscribe","",email,code))

    conn.commit()

    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(f"You've requested removal from random coffees.  To prove it really was you please enter the code below into the validation form.\n\nYour code is {code}\n\nIf it wasn't you please delete this message and move on with your life :-)")

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = f'Unsubscribe from Random Coffee Trial'
    msg['From'] = "Simon Andrews <simon.andrews@babraham.ac.uk>"
    msg['To'] = (f"{name} <{email}>")

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

    print(f"Content-type: text/plain\n")
    print(f"Action was sent email")

def validate(code):

    print("Code is "+code,file=sys.stderr)

    # Look for an entry in the database
    c = conn.cursor()

    c.execute("SELECT action,name,email FROM request WHERE secret=?",(code,))

    rows = c.fetchall()

    for row in rows:
        # There's probably only ever going to be one unless something
        # has gone horribly wrong, but what the heck
        action = row[0]
        name = row[1]
        email = row[2]

        if action=="subscribe":
            # Check they're not already subscribed
            c.execute("SELECT email FROM person WHERE email=?",(email,))
            existing = c.fetchall()
            if not existing:
                c.execute("INSERT INTO person (name,email) VALUES (?,?)",(name,email))
        
        elif action=="unsubscribe":
            c.execute("DELETE FROM person WHERE email=?",(email,))

        else:
            send_error(f"Unknown action {action}")
            break

    
    # Clean up
    c.execute("DELETE FROM request WHERE secret=?",(code,))

    conn.commit()

    print(f"Content-type: text/plain\n")
    print(f"Action was successful")


def random_code():
    code = []

    for _ in range(6):
        code.append(random.choice(string.ascii_letters + string.digits))

    return "".join(code)


if __name__ == "__main__":
    main()