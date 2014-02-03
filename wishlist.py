#!/usr/bin/env python3

import epyc
import html
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
	if not price:
		return price

	price = str(price)
	if re.match(r'^\$?\d{1,3}(,?\d{3})*(\.[0-9]+)?$', price):
		price = price.replace('$', '').replace(',', '')
		return "${0:,.2f}".format(float(price))

	return price

def display_name(user):
	return "%s %s (%s)" % (user.fname, user.lname, user.username)

def profile(response, username):
	logged_in = get_current_user(response)

	try:
		current_user = User.find(username)
	except UserNotFound:
		handle_error(response, message="Unable to find the specified user.")
		return

	user_lists = current_user.get_wishlists()

	if not user_lists:
		wishlist_name = "{}'s wishlist".format(username)
		Wishlist.create(wishlist_name, current_user)

		user_lists = current_user.get_wishlists()

	current_wishlist = user_lists[0]
	products = current_wishlist.get_items()

	for product in products:
		product.price = format_price(product.price)

	error_code = response.get_field('error')
	errors = []

	if error_code == '0':
		errors.append("Wish name cannot be empty")

	scope = {
		"username": username,
		"products": products,
		"listname": current_wishlist.list_name,
		"logged_in": logged_in,
		"current_user_fullname": display_name(current_user),
		"is_current_users_wishlist_page": is_current_users_wishlist_page(response, username),
		"response": response,
		"errors": errors,
		"profile_image_filename": '/static/images/profiles/%s' % current_user.image
	}

	if logged_in:
		logged_in_user = User.find(logged_in)

		scope["mutual_friend"] = logged_in_user.check_friend(current_user)
		scope["pending_friend_request"] = logged_in_user.check_pending_friend(current_user)
		scope["pending_friend_invite"] = current_user.check_pending_friend(logged_in_user)

	response.write(epyc.render("templates/wishlist.html", scope))

@logged_in
def add_item(response, username):
	user_lists = User.find(username).get_wishlists()
	current_wishlist = user_lists[0]

	details = {
		"name": response.get_field('wish'),
		"image": response.get_field('image') or '/static/images/gift_box.png',
		"link": response.get_field('website'),
		"description": response.get_field('description'),
		"price": response.get_field('price')
	}

	encoded_string = ""
	if details['name'] != "":
		product = Product.create(**details)
		current_wishlist.add_item(product)
	else:
		encoded_string = urlencode({'error': "0"})

	response.redirect('/users/' + username + "?" + encoded_string)

@logged_in
def delete_item(response, username, item_id):
	user_lists = User.find(username).get_wishlists()
	wishlist = user_lists[0]
	wishlist.delete_item(item_id)

	response.redirect('/users/' + username)

@logged_in
def edit_item(response, username, item_id):
	try:
		current_user = User.find(username)
	except UserNotFound:
		handle_error(response, message="Unable to find the specified user.")
		return

	if response.request.method == "POST":
		product = Product.find(item_id)

		product.name = response.get_field('wish')
		product.image = response.get_field('image') or '/static/images/gift_box.png'
		product.link = response.get_field('website') or None
		product.description = response.get_field('description') or None
		product.price = response.get_field('price') or None

		product.save()
		response.redirect("/users/" + username)
		return

	user_lists = current_user.get_wishlists()
	if not user_lists:
		handle_error(response, message="Unable to find the given user's wishlist.")
		return

	current_wishlist = user_lists[0]

	scope = {
		"username": username,
		"listname": current_wishlist.list_name,
		"logged_in": current_user,
		"current_user_fullname": display_name(current_user),
		"is_current_users_wishlist_page": is_current_users_wishlist_page(response, username),
		"product": Product.find(item_id)
	}

	response.write(epyc.render("templates/edit_item.html", scope))

@logged_in
def edit_user(response, username):
	try:
		current_user = User.find(username)
	except UserNotFound:
		handle_error(response, message="Unable to find the specified user.")
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

	response.redirect('/users/' + username)


def get_item(response, username, item_id):
	response.redirect("/users/" + username)

def home(response):
	scope = {"logged_in": get_current_user(response)}
	response.write(epyc.render("templates/home.html", scope))

def my_wishlist(response):
	if get_current_user(response):
		response.redirect("/users/" + get_current_user(response))
	else:
		response.redirect("/")

@logged_in
def add_friend(response, username):
	current_username = get_current_user(response)

	current = User.find(current_username)
	other = User.find(username)

	current.add_friend(other)
	response.redirect(response.get_field('redirect'))

@logged_in
def delete_friend(response, username):
	current_username = get_current_user(response)

	current = User.find(current_username)
	other = User.find(username)

	current.delete_friend(other)
	response.redirect(response.get_field('redirect'))

def handle_error(response, message=""):
	scope = {
		"logged_in": get_current_user(response),
		"message": message
	}

	response.write(epyc.render("templates/404.html", scope))

#@login.logged_in
def feed(response):
	response.write(epyc.render("templates/feed.html", {
		"productimage": "http://placekitten/150/150",
		"productname": "Green Socks",
		"firstname": "Marie",
		"lastname": "Atzarakis",
		"dob": "31st August"
	}))

def run_server(srvhost='', serverport=8888):
	server = Server(write_error=handle_error, hostname=srvhost, port=serverport)

	server.register('/users/([a-zA-Z0-9_]+)', profile)
	server.register('/users/([a-zA-Z0-9_]+)/item', add_item)
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
	server.register('/mywishlist', my_wishlist)
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
