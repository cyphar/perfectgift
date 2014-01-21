import sqlite3
from db.password import hashPw, saltGen

class UserNotFound(Exception):
	pass

class ProductNotFound(Exception):
	pass

class FriendAlreadyAdded(Exception):
	pass

_conn = sqlite3.connect("wishlist.db")

class User:
	def __init__(self, user_id, fname, lname, username, email, image=None, dob=None):
		self.user_id = user_id
		self.fname = fname
		self.lname = lname
		self.username = username
		self.email = email

		self.image = image or 'default.gif'
		self.dob = dob or None

	@classmethod
	def find_user(cls, username):
		cur = _conn.execute('''SELECT * FROM tbl_users WHERE username = ?''', (username,))
		row = cur.fetchone()
		if row is None:
			raise UserNotFound('{} does not exist'.format(username))

		####dob
		return User(row[0], row[1], row[2], row[3], row[4], row[5])

	@classmethod
	def find_user_with_user_id(cls, user_id):
		cur = _conn.execute('''SELECT * FROM tbl_users WHERE user_id = ?''', (user_id,))
		row = cur.fetchone()
		if row is None:
			raise UserNotFound('{} does not exist'.format(user_id))

		####dob
		return User(row[0], row[1], row[2], row[3], row[4], row[5])

	@classmethod
	def check_password(cls, username, password):
		try:
			cur = _conn.execute('''SELECT password, salt FROM tbl_users WHERE username = ? LIMIT 1''', (username,))
			row = cur.fetchone()
			if row:
				hashed_password = hashPw(password, row[1])
				if hashed_password[0] == row[0]:
					return True
			return False
		except UserNotFound:
			return False


	@classmethod
	def create_user(cls, fname, lname, username, email, password, image=None, dob=None):
		result = hashPw(password, saltGen())

		dob = dob or None
		image = image or 'default.gif'

		#####dob
		cur = _conn.execute('''INSERT INTO tbl_users (fname, lname, username, email, image, password, salt, dob) VALUES (?, ?, ?, ?, ?, ?, ?, date(?))''', (fname, lname, username, email, image, result[0], result[1], dob))
		_conn.commit()
		cur = _conn.execute('''SELECT last_insert_rowid()''')
		return User(cur.fetchone()[0], fname, lname, username, email, image, dob)

	@classmethod
	def delete_user(cls, username):
		cur = _conn.execute('''DELETE FROM t bl_users WHERE username = ?''', (username,))
		_conn.commit()

	def save(self):
		self.dob = self.dob or None
		self.image = self.image or 'default.gif'

		_conn.execute('''UPDATE tbl_users SET fname = ?, lname = ?, username = ?, email = ?, image = ?, dob = ? WHERE user_id = ?''',
					(self.fname, self.lname, self.username, self.email, self.image, self.dob, self.user_id))
		_conn.commit()

	def get_user_wish_lists(self):
		cur = _conn.execute('''SELECT * FROM tbl_wish_list WHERE user_id = ?''', (self.user_id,))
		rows = cur.fetchall()

		wishlists = []
		for i in rows:
			wishlist = Wishlist(i[0], i[1], i[2])
			wishlists.append(wishlist)
		return wishlists

	def get_profile_image(self):
		return '/static/images/profiles/' + self.image


	def create_wish_list (self, list_name):
		cur = _conn.execute('''INSERT INTO tbl_wish_list (list_name, user_id) VALUES ( ?, ?)''', (list_name, self.user_id)) #TODO salt function
		_conn.commit()
		cur = _conn.execute('''SELECT last_insert_rowid()''')
		return Wishlist(cur.fetchone()[0], list_name, self.user_id)

	def delete_wish_list (self, list_name):
		cur = _conn.execute('''DELETE FROM tbl_wish_list WHERE list_name = ? AND user_id = ?''', (list_name, self.user_id))
		_conn.commit()


	def delete_friend(self,  friend_id):
		cur = _conn.execute('''DELETE FROM tbl_friends
			WHERE f_user_id =? AND friend_id =?''', (self.user_id, friend_id))
		_conn.commit()

	def add_friend(self, friend_id):
		if(self.check_friend(friend_id) == False):
			cur = _conn.execute('''INSERT INTO tbl_friends VALUES (?,?)''', (self.user_id, friend_id))
			_conn.commit()
		else:
			raise FriendAlreadyAdded('Friend_id:.{} has already been added!'.format(friend_id))

	def check_friend(self, friend_id):
		cur = _conn.execute('''SELECT * FROM tbl_friends WHERE (f_user_id =? AND friend_id =?) OR (f_user_id =? AND friend_id =?) LIMIT 2''', (self.user_id, friend_id, friend_id, self.user_id))
		return len(cur.fetchall()) == 2 #if found exactly 2 rows

	def check_pending_friend(self, friend_id):
		cur = _conn.execute('''SELECT 1 FROM tbl_friends WHERE (f_user_id =? AND friend_id =?)''', (self.user_id, friend_id))
		return len(cur.fetchall()) > 0 #true if any rows returned

	def find_friends(self):
		cur = _conn.execute('''
			SELECT f_user_id FROM tbl_friends WHERE friend_id = ? INTERSECT
			SELECT friend_id FROM tbl_friends WHERE f_user_id = ?;
			''',(self.user_id, self.user_id))
		rows = cur.fetchall()
		return [i[0] for i in rows]

#	def edit_wish_list_name (self, list_name): add this in later version


# TODO make get_wish_list for the second iteration so friends can find friend's lists

class Product:
	def __init__(self, product_id, image, link, name, description, price, checked = 0):
		self.product_id = product_id
		self.image = image
		self.link = link
		self.name = name
		self.description = description
		self.price = price
		self.checked = checked


	@classmethod
	def find_product(cls, product_id):
		cur = _conn.execute('''SELECT * FROM tbl_products
			WHERE product_id=?''', (product_id,))
		row = cur.fetchone()
		if row is None:
			raise ProductNotFound('{} does not exist'.format(product_id))
		return Product(*row)

	@classmethod
	def create_product(cls, image, link, name, description, price):
		cur = _conn.execute('''INSERT INTO tbl_products (image,link,name,description,price) VALUES (?, ?, ?, ?, ?)''', (image, link, name, description, price))
		_conn.commit()
		cur = _conn.execute("SELECT last_insert_rowid()")
		return Product(cur.fetchone()[0], image, link, name, description, price)

	def update_product(self):
		cur = _conn.execute('''UPDATE tbl_products SET image=?, link=?, name=?, description=?, price=? WHERE product_id=?''', (self.image, self.link, self.name, self.description, self.price, self.product_id))
		_conn.commit()


class Wishlist:
	def __init__(self, wish_id, list_name, user_id):
		self.wish_id = wish_id
		self.list_name = list_name
		self.user_id = user_id

	def add_list_item (self, product_id):
		cur = _conn.execute('''INSERT INTO tbl_list_item (product_id, list_id, checked) VALUES(?, ?, 0)''', (product_id, self.wish_id))
		_conn.commit()


	def get_wish_list_products(self):
		cur = _conn.execute('''SELECT tbl_products.product_id, image, link, name, description, price, tbl_list_item.checked
							  FROM tbl_products, tbl_list_item, tbl_wish_list
							  WHERE tbl_products.product_id = tbl_list_item.product_id
							  AND tbl_list_item.list_id = tbl_wish_list.wish_id
							  AND wish_id = ?''', (self.wish_id,))
		rows = cur.fetchall()
		wishlistproducts = []
		for i in rows:
			if i[6] == 1:
				print("LOOK AT ME:", repr(i[6]))
			p = Product(i[0], i[1], i[2], i[3], i[4], i[5], i[6])
			wishlistproducts.append(p)
		return wishlistproducts

	def delete_list_item(self, product_id):
		cur = _conn.execute('''DELETE FROM tbl_list_item WHERE list_id=? AND product_id=?''', (self.wish_id, product_id))
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
