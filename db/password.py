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

import hashlib
import string
import random

users = {'Nick':('a60bd04d09d498fd5bd3f6b916045eaefd356737701f45aaee410ec76a19d340', '/Cv6<z^n'),	 #is cool
		 'Jon':('ece4f91a56ba8041965fddc79128ddf06c91332d6fea6a9062266f60e8e6cc50', '/_(pC]cW'),	#is 1337
		 'admin':('41c158da53e3a3a577074f39a654258bafb59320e38416b5c531dc0ba78fcfc6', '*\\,fZ>W>')}	#admin
#example user, {name:(hashedpass,salt),name2:(hashedpass2,salt2)}
#example password and salt generation:

#Gemerates a random salt and returns it
def generate_salt(size=8):
	valid_chars = string.ascii_letters + string.digits + '!#$%&\()*+,-./:;<=>?@[\\]^_`{|}~'
	return ''.join(random.choice(valid_chars) for i in range(size))


#hashPW('is cool',saltGen()) returns the hash for is cool along with the random salt used:
#ie	 hashPW('is cool',saltGen())
#		 ('a60bd04d09d498fd5bd3f6b916045eaefd356737701f45aaee410ec76a19d340', '/Cv6<z^n')
def hash_password(password, salt, rounds=7):
	for i in range(rounds):
		password = hashlib.sha256(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

	return password

#passcheck takes raw username and password as strings, and compares them to users dict
#returns True or False for correct or wrong login
#ie	 passCheck('Nick','is cool')
#		 True
#		 (duh)
'''
def check_password(username, password, rounds=1000):
	if username in users:

		salt = users[username][1]
		password = hash_password(users[username][0], )

		for i in range(rounds):
			password = hashlib.sha256(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

		if password == users[username][0]:
			return True

	return False
'''
