#!/usr/bin/env python3

import epyc
import html
import time
import json
import re
import argparse
import os

from tornado.ncss import Server

from login import *
from db.api import User, Wishlist, Product, UserNotFound

from urllib.parse import urlencode
from ajax import scrape

from friends import search, friends_list

def format_price(price):
	if re.match(r'^\$?\d{1,3}(,?\d{3})*(\.[0-9]+)?$', price):
		price = price.replace('$', '').replace(',', '')
		return "${0:,.2f}".format(float(price))
	return str(price)

def display_name(user):
  return "%s %s (%s)" % (user.fname, user.lname, user.username)

def index(response, username):
	logged_in = get_current_user(response)

	try:
		current_user = User.find_user(username)
	except UserNotFound:
		handle_error(response, message="user")
		return

	user_lists = current_user.get_user_wish_lists()

	if not user_lists:
		current_user.create_wish_list(str(username)+"'s wishlist")
		user_lists = current_user.get_user_wish_lists()
		#handle_error(response, message="wishlist for the given user")
		#return

	# TODO: user_lists index should be dynamicvalue
	current_wishlist = user_lists[0]
	products = current_wishlist.get_wish_list_products()
	for product in products:
		product.price = format_price(str(product.price))

	error_code = response.get_field('error')
	errors = []

	if error_code == '0':
		errors.append("Wish name cannot be empty")

	scope = {
		"username":username,
		"products": products,
		"listname": current_wishlist.list_name,
		"logged_in": logged_in,
		"current_user_fullname": display_name(current_user),
		"is_current_users_wishlist_page": is_current_users_wishlist_page(response, username),
		'response': response,
		'errors': errors,
		'profile_image_filename': '/static/images/profiles/%s' % current_user.image
	}

	if logged_in:
		logged_in_user = User.find_user(logged_in)
		scope["mutual_friend"] = logged_in_user.check_friend(current_user.user_id)
		scope["pending_friend_request"] = logged_in_user.check_pending_friend(current_user.user_id)
		scope["pending_friend_invite"] = current_user.check_pending_friend(logged_in_user.user_id)

	response.write(epyc.render("templates/wishlist.html", scope))

def edit(response, username): #WORKING HERE
	user_lists = User.find_user(username).get_user_wish_lists()
	current_wishlist = user_lists[0]
	products = current_wishlist.get_wish_list_products()
	scope = {"username":username, "products": products, "listname":current_wishlist.list_name, "logged_in": get_current_user(response)}
	response.write(epyc.render("templates/edit.html", scope))


def add_item(response, username):
	user_lists = User.find_user(username).get_user_wish_lists()
	# TODO: user_lists index should be dynamicvalue
	current_wishlist = user_lists[0]
	new_product_name = response.get_field('wish')
	new_link = response.get_field('website')
	new_description = response.get_field('description')
	new_price = response.get_field('price')
	new_image = response.get_field('image') or '/static/images/gift_box.png'
	encoded_string = ""
	if new_product_name is not "":
		is_error_msg_hidden = True
		new_product = Product.create_product(new_image, new_link, new_product_name, new_description, new_price)
		current_wishlist.add_list_item(new_product.product_id)
	else:
		encoded_string = urlencode({'error': "0"})

	response.redirect('/users/' + username + "?" + encoded_string)


def delete_item(response, username, item_id):
	user_lists = User.find_user(username).get_user_wish_lists()
	wishlist = user_lists[0]
	wishlist.delete_list_item(item_id)

	response.redirect('/users/' + username)

def edit_item(response, username, item_id):
	try:
		current_user = User.find_user(username)
	except UserNotFound:
		handle_error(response, message="user")
		return

	if response.request.method == "POST":
		product = Product.find_product(item_id)
		product.price = response.get_field('price')
		product.name = response.get_field('wish')
		product.description = response.get_field('description')
		product.link = response.get_field('website')
		product.image = response.get_field('image')
		product.update_product()
		response.redirect("/users/"+username)
		return

	user_lists = current_user.get_user_wish_lists()
	if not user_lists:
		handle_error(response, message="wishlist for the given user")
		return

	# TODO: user_lists index should be dynamicvalue
	current_wishlist = user_lists[0]
	scope = {"username":username,
            "listname": current_wishlist.list_name,
            "logged_in": current_user,
            "current_user_fullname": display_name(current_user),
            "is_current_users_wishlist_page": is_current_users_wishlist_page(response, username),
            "product": Product.find_product(item_id)
	}
	print(scope["product"].image)
	response.write(epyc.render("templates/edit.html", scope))

@logged_in
def edit_user(response, username):
	try:
		current_user = User.find_user(username)
	except UserNotFound:
		handle_error(response, message="user")
		return
	# supports image only for now, extend later for profile data changes

	filename, content_type, photo = response.get_file('profile-photo')
	accepted_image_formats = ['jpg', 'jpeg', 'JPEG', 'png', 'PNG', 'gif', 'GIF']

	if not filename or not content_type or not photo:
		if 'default' not in current_user.image.split('.'):
			old_image = 'static/images/profiles/' + current_user.image

			try:
				os.remove(old_image)
			except:
				pass

		current_user.image = None
		current_user.save()

		response.redirect('/users/' + username)
		return


	extension = filename.split('.')[-1]
	if extension in accepted_image_formats:
		img = "{}.{}".format(current_user.user_id, extension)
		profile_img = 'static/images/profiles/' + img

		if 'default' not in current_user.image.split('.'):
			old_image = 'static/images/profiles/' + current_user.image
			os.remove(old_image)

		current_user.image = img
		current_user.save()

		with open(profile_img, mode='wb') as f:
			f.write(photo)
			#time.sleep(1) # sleep briefly to ensure file is saved correctly on server

	response.redirect('/users/' + username)


def get_item(response, username, item_id):
	response.redirect("/users/"+username)

def home(response):
	response.write(epyc.render("templates/home.html", {"logged_in":get_current_user(response)}))

def myWishlist(response):
	if get_current_user(response):
		response.redirect("/users/" + get_current_user(response))
	else:
		response.redirect("/")


def add_friend(response, username):
	current_username = get_current_user(response)
	if not current_username:
		response.redirect("/login")
	else:
		current = User.find_user(current_username)
		other = User.find_user(username)
		current.add_friend(other.user_id)
		response.redirect(response.get_field('redirect'))

def delete_friend(response, username):
	current_username = get_current_user(response)
	if not current_username:
		response.redirect("/login")
	else:
		current = User.find_user(current_username)
		other = User.find_user(username)
		current.delete_friend(other.user_id)
		response.redirect(response.get_field('redirect'))

def handle_error(response, message='page'):
	response.write(epyc.render("templates/404.html", {"logged_in":get_current_user(response), "message":message}))

#@login.logged_in
def feed(response):
	response.write(epyc.render("templates/feed.html", {
		"productimage": "http://placekitten/150/150",
		"productname": "Green Socks",
		"firstname": "Marie",
		"lastname": "Atzarakis",
		"dob":"31st August"
		}))

def run_server(srvhost='', serverport=8888):
	server = Server(write_error=handle_error, hostname=srvhost, port=serverport)

	server.register('/users/([a-zA-Z0-9_]+)', index) #view users profile
	server.register('/users/([a-zA-Z0-9_]+)/item', add_item) #add item
	server.register('/users/([a-zA-Z0-9_]+)/item/([a-zA-Z0-9_]+)', get_item, delete=delete_item)
	server.register('/users/([a-zA-Z0-9_]+)/edit_item/([a-zA-Z0-9_]+)', edit_item)
	server.register('/users/([a-zA-Z0-9_]+)/edit', edit_user)
	server.register('/friends', friends_list)
	server.register('/add_friend/([a-zA-Z0-9_]+)', add_friend)
	server.register('/delete_friend/([a-zA-Z0-9_]+)', delete_friend)
	server.register('/login', login)
	server.register('/logout', logout)
	server.register('/signup', signup)
	server.register('/ajax/scrape', scrape.scrape_url)
	server.register('/', home)
	server.register('/mywishlist', myWishlist)
	server.register('/feed', feed)
	server.register('/search', search)
	server.register('.*', handle_error)

	server.run()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Start a tornado server, running the 'perfectgift.com' website.")
	parser.add_argument('-p', '--port', type=int, default=8888)
	parser.add_argument('-H', '--host', type=str, default='')
	args = parser.parse_args()

	run_server(args.host, args.port)
