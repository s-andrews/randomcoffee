#!/usr/bin/python3
import sqlite3
import random

def main():
    conn = sqlite3.connect("db/rct.db")

    c = conn.cursor()

    c.execute("SELECT email,name FROM person")

    people = c.fetchall()

    random.shuffle(people)

    person1 = None


    for person in people:
        if person1 is None:
            person1 = person
        
        else:
            match_pair(person1,person)
            person1 = None


    if person1:
        print(f"{person1[0]} is lonely")

def match_pair(p1,p2):
    print(f"{p1[0]} is matched with {p2[0]}")



if __name__ == "__main__":
    main()