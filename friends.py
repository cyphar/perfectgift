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
import sqlite3

from tornado.ncss import Server
from tornado.log import app_log

from db.api import User, Product, UserNotFound
from login import logged_in, get_current_user

@logged_in
def friends_list(response):
	current_username = get_current_user(response)
	current_user = User.find(current_username)

	friends_list = current_user.find_friends()

	scope = {'friends': friends_list, 'logged_in': current_username}
	response.write(epyc.render("templates/friends.html", scope))

def search(response):
	search = response.get_field("q")
	logged_in = get_current_user(response)

	types = {
		"people": 0,
		"items": 1
	}

	tp = types.get(response.get_field("t"), 0)

	if search:
		if tp == types['people']:
			items = User.search(search)
		else:
			items = Product.search(search)

		scope = {
			"query": search,
			"results": items,
			"tp": tp,
			"types": types,
			"logged_in": get_current_user(response)
		}

		app_log.info("[%s found for '%s'] %s" % (response.get_field('t'), search, items))
		response.write(epyc.render("templates/search.html", scope))

	else:
		scope = {
			"query": "",
			"results": [],
			"tp": tp,
			"types": types,
			"logged_in": get_current_user(response)
		}

		response.write(epyc.render("templates/search.html", scope))

def hello(response, match):
	response.write(epyc._render('''
	<html>
	<header>:)</header>
	<body>
	<h1>Hellos peoples of the internets</h1>
	</body>
	</html>
'''))

if __name__ == '__main__':
	server=Server()
	server.register('/search',search)
	server.register('/friends/([a-zA-Z0-9_]+)', friends_list)
	server.run()
