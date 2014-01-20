#!/usr/bin/env python3

import re
import os
import sqlite3

from random import randint
from password import hashPw, saltGen

def generate_user_row(conn, fname, lname, username, email, passw, dob):
	#user_row = "INSERT INTO tbl_users (fname, lname, username, email, password, salt) VALUES (		0, 'Barry', 'Schultz', 'bazS', 'bazS@here.now', '3a3b2372dd1f0c0f5e8bdd3196bb29dbcbd7f75a55abb9ba9ab2f60243bcd517', 'x_HCV[`/', '1997-09-01')"
	p, salt = hashPw(passw, saltGen())
	user_row = "INSERT INTO tbl_users (fname, lname, username, email, password, salt, dob) VALUES(?,?,?,?,?,?, ?)"
	try:
		conn.execute(user_row, (fname, lname, username, email, p, salt, dob ))
	except sqlite3.IntegrityError:
		pass

def getpath(fname):
	dirname = os.path.dirname(__file__)
	return os.path.join(dirname, fname)

def initdb():
	open("wishlist.db", "w")
	conn = sqlite3.connect("wishlist.db")

	script = ""

	with open(getpath("clean.sql")) as f:
		script += f.read()

	with open(getpath("init.sql")) as f:
		script += f.read()

	with open(getpath("fake.sql")) as f:
		script += f.read()

	conn.executescript(script)
	conn.commit()

	#populate users
	names = []
	emails = []
	usernames = []
	passwords = []

	with open(getpath("random_names.txt")) as n:
		for j in n:
			j = j.rstrip()
			names.append(j)

	for i in names:
		email = i + str(randint(0,10)) + str(randint(0,10)) +str(randint(0,10)) +str(randint(0,10)) +"@.yoloteamfour.com"
		emails.append(email)
		username = i[:randint(2,4)] + str(randint(0,10))
		usernames.append(username)
		password = i[::-1]
		passwords.append(password)

	i = 0
	while i < len(emails):
		random_num = randint(0, len(names) -1 )
		fname_index = names[randint(0,len(names) - 1)]
		lname_index = names[randint(0,len(names) - 1)]
		username_index = usernames[random_num]
		email_index = emails[random_num]
		password_index = passwords[random_num]
		generate_user_row(conn, fname_index, lname_index, username_index, email_index, password_index, str(randint(1900,2000)) + "-" + str(randint(0, 12)) + "-" + str(randint(0, 31)))
		i += 1

	conn.commit()
	conn.close()

if __name__ == "__main__":
	initdb()
	#import cProfile
	#print(cProfile.run("initdb()"))
