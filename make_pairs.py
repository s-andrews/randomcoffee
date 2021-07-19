#!/usr/bin/python3
import sqlite3
import random

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

        print("Searching for pairs")
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
                    print(f"Found previous pair {person1[1]} and {person[1]}")
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
        emailpair = [x[1].lower() for x in pair]
        emailpair.sort()
        emailpair = ":".join(emailpair)
        c.execute("INSERT INTO pairing (emailpair) VALUES (?)",(emailpair,))

    conn.commit()

    for pair in pairs:
        print(pair[0][1]+" matched with "+pair[1][1])


def seen_before(p1,p2,c):
    emailpair = [p1[1].lower(),p2[1].lower()]
    emailpair.sort()
    emailpair = ":".join(emailpair)

    c.execute("SELECT * FROM pairing WHERE emailpair=?",(emailpair,))

    if c.fetchall():
        return True

    return False




if __name__ == "__main__":
    main()