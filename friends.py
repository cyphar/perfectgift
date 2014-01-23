import epyc
import sqlite3

from tornado.ncss import Server
from tornado.log import app_log

from db.api import User, UserNotFound
from login import  logged_in, get_current_user

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

	if search:
		if response.get_field("searchr") == 'people':
			items = User.search(search)
			scope = {
				"query": search,
				"no_results": len(items) == 0,
				"results_people": items,
				"people_checked": "checked",
				"items_checked": "",
				"logged_in": get_current_user(response)
			}

			app_log.info("[people found for '%s'] %s" % (search, items))
			response.write(epyc.render("templates/search.html", scope))
		elif response.get_field("searchr") == 'items':
			items = Product.search(search)
			scope = {
				"query": search,
				"no_results": len(items) == 0,
				"results_items": items,
				"people_checked": "",
				"items_checked": "checked",
				"logged_in": get_current_user(response)
			}

			app_log.info("[items found for '%s'] %s" % (search, items))
			response.write(epyc.render("templates/search.html", scope))
	else:
		people_or_item = response.get_field("searchr")
		scope = {
			"query": "",
			"no_results": False,
			"results": None,
			"people_checked": "",
			"items_checked": "",
			"logged_in": get_current_user(response)
		}

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
