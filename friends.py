import epyc
import sqlite3
import locale

from tornado.ncss import Server
from db.api import User, UserNotFound
from login import  logged_in, get_current_user

conn = sqlite3.connect("wishlist.db")
locale.setlocale(locale.LC_ALL, '')

@logged_in
def friends_list(response):
	current_username = get_current_user(response)
	current_user = User.find(current_username)

	friends_list = current_user.find_friends()

	scope = {'friends': friends_list, 'logged_in': current_username}
	response.write(epyc.render("templates/friends.html", scope))

def search(response):
	search = response.get_field("search")
	logged_in = get_current_user(response)

	if response.get_field("search"):
		if response.get_field("searchr") == 'people':
			friend_sea = "%{}%".format("".join(search))

			# XXX: MIGRATE TO DATABASE API!!!
			cur = conn.execute('''SELECT fname, lname, username FROM tbl_users WHERE username like ? or fname like ? or lname like ?''', (friend_sea, friend_sea, friend_sea))
			rows = cur.fetchall()

			row2 = []

			for row in  rows:
				row = " ".join(row)
				row2.append(row)

			response.write(epyc.render("templates/search.html", {"query": search, "no_results": len(row2) == 0, "results_people": row2, "people_checked": "checked", "items_checked":"", "logged_in": get_current_user(response)}))
		elif response.get_field("searchr") == 'items':
			item_sea = "%{}%".format(search)

			cur = conn.execute('''SELECT image, name, description, price, link from tbl_products WHERE name like (?)''', (item_sea,))
			rows = cur.fetchall()

			row2 = []
			for row in rows:
				row_short = []
				for i in range(len(row)):
					if i == 3:
						row_short.append(locale.currency(row[i]))
					else:
						row_short.append(row[i])
				row2.append(row_short)

			response.write(epyc.render("templates/search.html", {"query": search, "no_results": True, 'results_items': row2, "people_checked": "", "items_checked":"checked","logged_in": get_current_user(response)}))
	else:
		people_or_item = response.get_field("searchr")
		scope = {"query": "", "no_results": False, "results": None, "people_checked": "", "items_checked": "", "logged_in": get_current_user(response)}

		if people_or_item == "items":
			scope["items_checked"] = "checked"
		else:
			scope["people_checked"] = "checked"

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
