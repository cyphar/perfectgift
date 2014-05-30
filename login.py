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

import epyc
import re

from tornado.ncss import Server
from db.api import User, Wishlist, UserNotFound

# decorator function for checking that the user is logged in
def logged_in(func, url='/login'):
	def inner(response, *args, **kwargs):
		userid = response.get_secure_cookie('userid')

		if userid:
			return func(response, *args, **kwargs)

		response.redirect(url)
	return inner

def get_current_user(response):
	userid = response.get_secure_cookie('userid')

	if userid:
		userid = userid.decode("utf-8")
	else:
		userid = None

	return userid

#@logged_in
def is_current_users_wishlist_page(response, username):
	if get_current_user(response) == username:
		return True
	return False

def login(response):
	uid = response.get_field("uid")
	pwd = response.get_field("pwd", strip=False)
	userid = response.get_secure_cookie('userid')

	# already logged in!
	if userid:
		response.redirect('/users/' + userid.decode('utf-8'))
		return

	elif uid is None or pwd is None:
		scope = {"logged_in": get_current_user(response)}
		response.write(epyc.render("templates/login.html", scope))
		return

	errors = []

	if not uid or not pwd:
		errors.append("Empty username or password")

	elif not User.check_password(uid, pwd):
		errors.append("Incorrect username or password")

	if errors:
		scope = {
			"errors": errors,
			"logged_in": get_current_user(response)
		}

		response.write(epyc.render("templates/login.html", scope))

	else:
		response.set_secure_cookie('userid', uid)
		response.redirect('/users/%s' % uid)

def logout(response):
	response.clear_cookie("userid")
	response.redirect('/')

def signup(response):
	fname = response.get_field("fname")
	lname = response.get_field("lname")
	email = response.get_field("email")
	username = response.get_field("username")
	password = response.get_field("password")
	# check for invalid input

	errors = []

	if not fname:
		errors.append("First name required")

	if not lname:
		errors.append("Last name required")

	if not re.match(r"^[-a-zA-Z0-9+\._]+@([-a-zA-Z0-9]+\.)+[a-zA-Z]+$", email):
		errors.append("Valid email address required")

	if not re.match(r"^[a-zA-Z0-9_]+$", username):
		errors.append("Username can only contain letters, numbers or underscores")

	if len(password) < 6:
		errors.append("Password must be longer than 5 characters")

	if not errors:
		try:
			User.find(username)
		except UserNotFound:
			pass
		else:
			errors.append("Username is taken")

	if errors:
		scope = {
			"errors": errors,
			"logged_in": get_current_user(response),
			"fname": fname,
			"lname": lname,
			"email": email,
			"username": username
		}

		response.write(epyc.render("templates/login.html", scope))

	else:

		user = User.create(fname, lname, username, email, password)
		response.set_secure_cookie('userid', user.username)

		listname = "{}'s wishlist".format(user.username)
		Wishlist.create(listname, user)

		response.redirect('/users/' + user.username)
