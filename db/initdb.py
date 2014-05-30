#!/usr/bin/env python3
# perfectgift: a tornado webapp for creating wish lists between friends
# Copyright (C) 2014, NCSS14 Group 4

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# 1. The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import os
import sqlite3
import random
import argparse

from password import hash_password, generate_salt

def getpath(fname):
	dirname = os.path.dirname(__file__)
	return os.path.join(dirname, fname)

def generate_fake_users(conn):
	names = []
	with open(getpath("random_names.txt")) as f:
		names = [name.strip() for name in f]

	for i in range(len(names)):
		fname, lname = random.sample(names, 2)
		username = (fname[0] + lname).lower()

		email = "{}{:03}@yoloteamfour.com".format(username, random.randint(0, 100))

		salt = generate_salt()
		password = username[::-1]
		password = hash_password(password, salt)

		dob = "{:04}-{:02}-{:02}".format(random.randint(1970, 2000), random.randint(1, 12), random.randint(1, 28))

		try:
			conn.execute("""INSERT INTO tbl_users (fname, lname, username, email, password, salt, dob) VALUES (?, ?, ?, ?, ?, ?, strftime('%s', ?))""",
					(fname, lname, username, email, password, salt, dob))
		except sqlite3.IntegrityError:
			pass

	conn.commit()

def initdb(dbfile='wishlist.db', fake=True):
	# Clear the file.
	with open(dbfile, "w") as f:
		pass

	conn = sqlite3.connect(dbfile)
	script = ""

	with open(getpath("clean.sql")) as f:
		script += f.read()

	with open(getpath("init.sql")) as f:
		script += f.read()

	conn.executescript(script)
	conn.commit()

	if fake:
		with open(getpath("fake.sql")) as f:
			conn.executescript(f.read())
			conn.commit()

		generate_fake_users(conn)

	conn.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Generate the 'perfectgift.com' sqlite database.")
	parser.add_argument('-d', '--dbfile', help="path to database file to be created", type=str, default='wishlist.db')
	parser.add_argument('-f', '--fake', help="generate fake users, wishlists, products and friends", action="store_true")
	args = parser.parse_args()

	initdb(args.dbfile, args.fake)
	#import cProfile
	#print(cProfile.run("initdb()"))
