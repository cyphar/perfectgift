import sqlite3
from db.password import hash_password, generate_salt

class UserNotFound(Exception):
	pass

class ProductNotFound(Exception):
	pass

class FriendAlreadyAdded(Exception):
	pass

_conn = sqlite3.connect("wishlist.db")
_conn.row_factory = sqlite3.Row

class User:
	def __init__(self, user_id, fname, lname, username, email, image=None, dob=None):
		self.user_id = user_id
		self.fname = fname
		self.lname = lname
		self.username = username
		self.email = email

		self.image = image or 'default.gif'
		self.dob = dob or None

	#################
	# CLASS METHODS #
	#################

	@classmethod
	def find(cls, username):
		cur = _conn.execute('''SELECT user_id, fname, lname, username, email, image, dob FROM tbl_users WHERE username = ? LIMIT 1''', (username,))
		row = cur.fetchone()

		if not row:
			print("Cannot find {}".format(username))
			raise UserNotFound('Username {} does not exist'.format(username))

		return cls(**row)

	@classmethod
	def find_uid(cls, user_id):
		cur = _conn.execute('''SELECT user_id, fname, lname, username, email, image, dob FROM tbl_users WHERE user_id = ? LIMIT 1''', (user_id,))
		row = cur.fetchone()

		if not row:
			raise UserNotFound('Uid {} does not exist'.format(user_id))

		return cls(**row)

	@classmethod
	def create(cls, fname, lname, username, email, password, image=None, dob=None):
		salt = generate_salt()
		password_hash = hash_password(password, salt)

		dob = dob or None
		image = image or 'default.gif'

		_conn.execute('''INSERT INTO tbl_users (fname, lname, username, email, image, password, salt, dob) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (fname, lname, username, email, image, password_hash, salt, dob))
		_conn.commit()

		return cls.find(username)

	@classmethod
	def check_password(cls, username, password):
		cur = _conn.execute('''SELECT password, salt FROM tbl_users WHERE username = ? LIMIT 1''', (username,))
		row = cur.fetchone()

		if not row:
			return False

		salt = row['salt']
		password_hash = hash_password(password, salt)

		if password_hash == row['password']:
			return True

		return False

	#######################
	# MODIFY USER METHODS #
	#######################

	def delete(self):
		_conn.execute('''DELETE FROM tbl_users WHERE user_id = ?''', (self.user_id,))
		_conn.commit()

	def save(self):
		self.dob = self.dob or None
		self.image = self.image or 'default.gif'

		_conn.execute('''UPDATE tbl_users SET fname = ?, lname = ?, username = ?, email = ?, image = ?, dob = ? WHERE user_id = ?''', (self.fname, self.lname, self.username, self.email, self.image, self.dob, self.user_id))
		_conn.commit()

	# TODO: Put this in some globals file.
	def get_profile_image(self):
		return '/static/images/profiles/' + self.image

	####################
	# WISHLIST METHODS #
	####################

	def add_wishlist(self, list):
		_conn.execute('''INSERT INTO tbl_wish_list (list_name, user_id) VALUES (?, ?)''', (list_name, self.user_id))
		_conn.commit()

		cur = _conn.execute('''SELECT last_insert_rowid()''')
		return Wishlist(cur.fetchone()['wish_id'], list_name, self.user_id)

	def delete_wish_list(self, list_name):
		_conn.execute('''DELETE FROM tbl_wish_list WHERE list_name = ? AND user_id = ?''', (list_name, self.user_id))
		_conn.commit()

	def get_wishlists(self):
		cur = _conn.execute('''SELECT wish_id, list_name FROM tbl_wish_list WHERE user_id = ?''', (self.user_id,))
		rows = cur.fetchall()

		wishlists = []

		for row in rows:
			wishlist = Wishlist(user=self, **row)
			wishlists.append(wishlist)

		return wishlists

	##################
	# FRIEND METHODS #
	##################

	def delete_friend(self, friend):
		_conn.execute('''DELETE FROM tbl_friends WHERE (f_user_id = ? AND friend_id = ?) OR (f_user_id = ? AND friend_id = ?)''', (self.user_id, friend_id, friend_id, self.user_id))
		_conn.commit()

	def add_friend(self, friend):
		if not self.check_friend(friend_id) == False:
			_conn.execute('''INSERT INTO tbl_friends (f_user_id, friend_id) VALUES (?, ?)''', (self.user_id, friend.user_id))
			_conn.commit()
		else:
			raise FriendAlreadyAdded('{} has already been added as a friend of {}'.format(friend.username, self.username))

	def check_friend(self, friend_id):
		cur = _conn.execute('''SELECT COUNT(*) FROM tbl_friends WHERE (f_user_id = ? AND friend_id = ?) OR (f_user_id = ? AND friend_id = ?)''', (self.user_id, friend_id, friend_id, self.user_id))
		count = cur.fetchone()[0]

		return count == 2

	def check_pending_friend(self, friend_id):
		cur = _conn.execute('''SELECT COUNT(*) FROM tbl_friends WHERE f_user_id = ? AND friend_id = ?''', (self.user_id, friend_id))
		count = cur.fetchone()[0]

		return count > 0

	def find_friends(self):
		cur = _conn.execute('''SELECT f_user_id FROM tbl_friends WHERE friend_id = ? INTERSECT SELECT friend_id FROM tbl_friends WHERE f_user_id = ?''',(self.user_id, self.user_id))
		rows = cur.fetchall()

		return [User.find_uid(row['f_user_id']) for row in rows]


class Product:
	def __init__(self, product_id, name, image, link, description, price, checked=0):
		self.product_id = product_id
		self.name = name
		self.image = image or '/static/images/gift_box.png'
		self.link = link
		self.description = description
		self.price = price
		self.checked = checked or 0

	#################
	# CLASS METHODS #
	#################

	@classmethod
	def find(cls, product_id):
		cur = _conn.execute('''SELECT p.product_id, p.name, p.image, p.link, p.description, p.price, i.checked FROM tbl_products AS p LEFT JOIN tbl_list_item AS i ON p.product_id = i.product_id WHERE p.product_id = ? LIMIT 1''', (product_id,))
		row = cur.fetchone()

		if not row:
			raise ProductNotFound('{} does not exist'.format(product_id))

		return cls(*row)

	@classmethod
	def create(cls, name, image, link, description, price):
		_conn.execute('''INSERT INTO tbl_products (name, image, link, description, price) VALUES (?, ?, ?, ?, ?)''', (name, image, link, description, price))
		_conn.commit()

		cur = _conn.execute("SELECT last_insert_rowid()")
		product_id = cur.fetchone()[0]

		return cls.find(product_id)

	##########################
	# PRODUCT MODIFY METHODS #
	##########################

	def save(self):
		print("%r %r %r %r" % (self.name, self.image, self.link, self.description))
		_conn.execute('''UPDATE tbl_products SET name = ?, image = ?, link = ?, description = ?, price = ? WHERE product_id = ?''', (self.name, self.image, self.link, self.description, self.price, self.product_id))
		_conn.commit()

	def delete(self):
		_conn.execute('''DELETE FROM tbl_products WHERE product_id = ?''', (self.product_id,))
		_conn.commit()


class Wishlist:
	def __init__(self, wish_id, list_name, user):
		self.wish_id = wish_id
		self.list_name = list_name
		self.user = user

	#################
	# CLASS METHODS #
	#################

	@classmethod
	def find(cls, wish_id):
		cur = _conn.execute('''SELECT wish_id, list_name, user_id FROM tbl_wish_list WHERE wish_id = ? LIMIT 1''', (wish_id,))

		wish_id, list_name, user_id = cur.fetchone()
		user = User.find_uid(user_id)

		return cls(wish_id, list_name, user)

	@classmethod
	def create(cls, list_name, user):
		_conn.execute('''INSERT INTO tbl_wish_list (list_name, user_id) VALUES (?, ?)''', (list_name, user.user_id))
		_conn.commit()

		cur = _conn.execute('''SELECT last_insert_rowid()''')
		wish_id = cur.fetchone()[0]

		return cls.find(wish_id)

	###########################
	# WISHLIST MODIFY METHODS #
	###########################

	def delete(self):
		_conn.execute('''DELETE FROM tbl_wish_list WHERE wish_id = ?''', (self.wish_id,))
		_conn.commit()

	def save(self):
		_conn.execute('''UPDATE tbl_wish_list SET list_name = ?, user_id = ? WHERE wish_id = ?''', (self.list_name, self.user.user_id, self.wish_id))
		_conn.commit()

	def add_item(self, product):
		_conn.execute('''INSERT INTO tbl_list_item (product_id, list_id, checked) VALUES(?, ?, 0)''', (product.product_id, self.wish_id))
		_conn.commit()

	def get_items(self):
		cur = _conn.execute('''SELECT tbl_products.product_id, name, image, link, description, price, tbl_list_item.checked
							  FROM tbl_products, tbl_list_item, tbl_wish_list
							  WHERE tbl_products.product_id = tbl_list_item.product_id
							  AND tbl_list_item.list_id = tbl_wish_list.wish_id AND wish_id = ?''', (self.wish_id,))
		rows = cur.fetchall()

		items = []
		for row in rows:
			p = Product(*row)
			items.append(p)

		return items

	def delete_item(self, product_id):
		_conn.execute('''DELETE FROM tbl_list_item WHERE list_id = ? AND product_id = ?''', (self.wish_id, product_id))
		_conn.commit()

####USERS####

#find a user
#uf = User.find_user("matN")
#u = User.find_user("bazS")
#print(u.find_friends())

#get the user's wishlist



#create a user
#u = User.create_user("Poo", "Nick", "Winnie12", "akdjsrgsegrsedfsd@poo.com", "12234")
#check a password
#print(User.check_password("Winnie12","12234"))

#delete a user
#User.delete_user("matN")


####PRODUCTS####
#find product
#p = Product.find_product(1)

#create a product
#p = Product.create_product("blah.jpg", "http://teamfourftw.com", "blah", "This is a description", 100000)

####WISHLIST####


#create a wishlist
#u = User.find_user("karB")
#w = u.create_wish_list("birthday")

#delete the wishlist
#u.delete_wish_list("birthday")

#gets a user's wishlists
#w = u.get_user_wish_lists()

#gets all products for a specific wishlist
#print(w.get_wish_list_products()[0].name)


####LIST ITEM####
#Add a list item
#w.add_list_item(1)


#get all products of a specific list
#print(w.get_wish_list_products())
