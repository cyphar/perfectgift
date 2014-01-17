import hashlib
import string
import random

availChars = string.ascii_letters + string.digits + '!#$%&\()*+,-./:;<=>?@[\\]^_`{|}~'
users = {'Nick':('a60bd04d09d498fd5bd3f6b916045eaefd356737701f45aaee410ec76a19d340', '/Cv6<z^n'),   #is cool
		 'Jon':('ece4f91a56ba8041965fddc79128ddf06c91332d6fea6a9062266f60e8e6cc50', '/_(pC]cW'),	#is 1337
		 'admin':('41c158da53e3a3a577074f39a654258bafb59320e38416b5c531dc0ba78fcfc6', '*\\,fZ>W>')}  #admin
#example user, {name:(hashedpass,salt),name2:(hashedpass2,salt2)}
#example password and salt generation:

#Gemerates a random salt and returns it
def saltGen():
	return (''.join(random.choice(availChars) for i in range(8)))


#hashPW('is cool',saltGen()) returns the hash for is cool along with the random salt used:
#ie	 hashPW('is cool',saltGen())
#	   ('a60bd04d09d498fd5bd3f6b916045eaefd356737701f45aaee410ec76a19d340', '/Cv6<z^n')
def hashPw(password, salt):
	for i in range(7):
		password = (hashlib.sha256(password.encode('utf-8') + salt.encode('utf-8'))).hexdigest()
	return password, salt


#passcheck takes raw username and password as strings, and compares them to users dict
#returns True or False for correct or wrong login
#ie	 passCheck('Nick','is cool')
#	   True
#	   (duh)
def passCheck(username, password):
	if username in users:
		salt = users[username][1]
		for i in range(7):
			password = (hashlib.sha256(password.encode('utf-8') + salt.encode('utf-8'))).hexdigest()
		if password == users[username][0]:
			return True
	return False
