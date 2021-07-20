#!/usr/bin/python3
import sqlite3
import random
from email.message import EmailMessage
import smtplib

def main():
    conn = sqlite3.connect("db/rct.db")

    c = conn.cursor()
    c.execute("SELECT email,name FROM person")
    people = c.fetchall()

    found_previous_pair = True

    # This is nastily inefficient in that we just try pairing 
    # everyone and we give up as soon as we hit a previous
    # pairing.  It'll work well enough for now but we'll need 
    # to be more efficient eventually.

    iteration_count = 0
    while found_previous_pair:

        found_previous_pair = False
        iteration_count += 1

        random.shuffle(people)
        person1 = None

        pairs = []

        for person in people:
            if person1 is None:
                person1 = person
            
            else:
                if seen_before(person1,person,c):
                    # print(f"Found previous pair {person1[1]} and {person[1]}")
                    found_previous_pair = True
                    break

                pairs.append([person1,person])
                person1 = None

        if not found_previous_pair and person1:
            print(f"{person1[0]} is lonely")

        if not found_previous_pair:
            print(f"Found pairings in {iteration_count} iterations")

    # Add the pairings to the database
    for pair in pairs:
        emailpair = [x[0].lower() for x in pair]
        emailpair.sort()
        emailpair = ":".join(emailpair)
        c.execute("INSERT INTO pairing (emailpair) VALUES (?)",(emailpair,))

    conn.commit()

    for pair in pairs:
        print(pair[0][1]+" matched with "+pair[1][1])

    send_email(("simon.andrews@babraham.ac.uk","Simon Andrews"),("babraham.bioinformatics@babraham.ac.uk","Babraham Bioinformatics"))



def seen_before(p1,p2,c):
    emailpair = [p1[0].lower(),p2[0].lower()]
    emailpair.sort()
    emailpair = ":".join(emailpair)

    c.execute("SELECT * FROM pairing WHERE emailpair=?",(emailpair,))

    if c.fetchall():
        return True

    return False


def send_email(person1, person2):
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(f"""
Hi {person1[1]} and {person2[1]},

Please meet your latest random coffee partner. 

You've been automatically paired up, but from here it's up to you to arrange an actual date and time to meet up, either in person or virtually.

The Random Coffee Robot.
-- 
You can unsubscribe from these messages at any point by going to https://www.bioinformatics.babraham.ac.uk/rct/ and clicking on the unsubscribe button. Any comments or suggestions about this projcet, please email elizabeth.wynn@babraham.ac.uk. Any technical problems, please email simon.andrews@babraham.ac.uk
""")

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = f'Your Random Coffee Match!'
    msg['From'] = "Random Coffee <babraham.bioinformatics@babraham.ac.uk>"
    msg['To'] = (f"{person1[1]} <{person1[0]}>, {person2[1]} <{person2[0]}>")


    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()




if __name__ == "__main__":
    main()