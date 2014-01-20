#!/usr/bin/env python3

import re
from random import randint
from password import hashPw, saltGen
import sqlite3

def generate_user_row(conn, fname, lname, username, email, passw, dob):
	#user_row = "INSERT INTO tbl_users (fname, lname, username, email, password, salt) VALUES (		0, 'Barry', 'Schultz', 'bazS', 'bazS@here.now', '3a3b2372dd1f0c0f5e8bdd3196bb29dbcbd7f75a55abb9ba9ab2f60243bcd517', 'x_HCV[`/', '1997-09-01')"
	p, salt = hashPw(passw, saltGen())
	user_row = "INSERT INTO tbl_users (fname, lname, username, email, password, salt, dob) VALUES(?,?,?,?,?,?, ?)"
	try:
		conn.execute(user_row, (fname, lname, username, email, p, salt, dob ))
	except sqlite3.IntegrityError:
		pass

def initdb():
	open("wishlist.db", "w")

	sqlscript = '''
	DROP TABLE if exists tbl_users;
	DROP TABLE if exists tbl_products;
	DROP TABLE if exists tbl_friends;
	DROP TABLE if exists tbl_wish_list;
	DROP TABLE if exists tbl_list_item;

	CREATE TABLE tbl_users (
		user_id INTEGER NOT NULL ,
		fname TEXT NOT NULL,
		lname TEXT NOT NULL,
		username TEXT NOT NULL UNIQUE,
		email TEXT NOT NULL UNIQUE,
		password TEXT NOT NULL,
		salt TEXT NOT NULL,
		dob TEXT,
		PRIMARY	KEY (user_id)
	);

	CREATE TABLE tbl_products (
		product_id INTEGER NOT NULL,
		image TEXT,
		link TEXT,
		name TEXT NOT NULL,
		description TEXT,
		price DOUBLE,
		PRIMARY KEY (product_id)
	);

	CREATE TABLE tbl_friends (
		f_user_id INTEGER NOT NULL,
		friend_id INTEGER NOT NULL,
		PRIMARY KEY (f_user_id, friend_id),
		FOREIGN KEY (friend_id) REFERENCES tbl_users,
		FOREIGN KEY (f_user_id) REFERENCES tbl_users
	);

	CREATE TABLE tbl_wish_list (
		wish_id INTEGER NOT NULL,
		list_name TEXT NOT NULL,
		user_id INTEGER NOT NULL,
		PRIMARY KEY (wish_id),
		FOREIGN KEY (user_id) REFERENCES tbl_users
	);

	CREATE TABLE tbl_list_item (
		list_id INTEGER NOT NULL,
		product_id INTEGER NOT NULL,
		checked INTEGER NOT NULL,
		PRIMARY KEY (list_id, product_id),
		FOREIGN KEY (product_id) REFERENCES tbl_products,
		FOREIGN KEY (list_id) REFERENCES tbl_wish_list
	);

	INSERT INTO tbl_users VALUES (		0, 'Barry', 'Schultz', 'bazS', 'bazS@here.now', '3a3b2372dd1f0c0f5e8bdd3196bb29dbcbd7f75a55abb9ba9ab2f60243bcd517', "x_HCV[`/", "1997-09-01");
	INSERT INTO tbl_users VALUES (		1, 'Prue', 'Robinson', 'pruR', 'pruR@here.now', 'f19ac3fa320b096735b4f734aba6550734213a35c28bdcec4eed5a78157daf14', "y{DZp?uc", "1997-09-01" );
	INSERT INTO tbl_users VALUES (		2, 'Andrew', 'Varvel', 'andV', 'andV@here.now', 'e5aabf82efd3ea15d803e2190a18e3131b22c2f013dcf8a9d600b5f06cd0242d', "(cFg^KtE", "1997-09-01");
	INSERT INTO tbl_users VALUES (		3, 'Mathew', 'Nemes', 'matN', 'matN@here.now', '05acaabdba3907e829b330f81c8b3deace38ccbefa1ef795534107d15eee95e1', "i]xs@K\\W", "1997-09-01");
	INSERT INTO tbl_users VALUES (		4, 'Mara', 'Barber', 'marB', 'marB@here.now', '307f8f39111c1988983953b24a343e91222df1edccfd95e809b31268cf1f54a4', "VoAqaR1i", "1997-09-01");
	INSERT INTO tbl_users VALUES (		5, 'Scott', 'Herdman', 'scoH', 'scoH@here.now', '0f6d189941215610b505b9354d47ae33431e00546ba9f4afc92b39f9c381e4fc', "E-G,M%UZ", "1997-09-01");
	INSERT INTO tbl_users VALUES (		6, 'Alec', 'Newton', 'aleN', 'aleN@here.now', '8f71b161b562d7c0d3b01babcd454cbd4b9319b8b92a1d555dde614a79a29e23', "SVe>88P.", "1997-09-01");
	INSERT INTO tbl_users VALUES (		7, 'Karen', 'Barber', 'karB', 'karB@here.now', '052b43fd7391614896cb2cf37eae4a0fb514a25b55731809a169fd0e72ccb84c', ",5&ud,[q", "1997-09-01");
	INSERT INTO tbl_users VALUES (		8, 'Grant', 'Ovzinsky', 'granO', 'granO@here.now', '1c9fe0f03bfd50c9df89a42e27f7041606d8c8b49e102e645628c57ef5ea2d25', "ev\\0Qqb2", "1997-09-01");
	INSERT INTO tbl_users VALUES (		9, 'Nick', 'Wright', 'admin', 'admin@group4.com', 'd86a0c720b776de00005283374c17fa3243094d2aa482db36f6311bc801e9f2f', 'z(z6|Z3Q', '1997-09-01');

	INSERT INTO tbl_products VALUES (		0, '/static/images/gift_box.png', 'http://www.smiley.com', 'smiley pillow', 'cutesy smiley pillow at MYER', 2014.0 );
	INSERT INTO tbl_products VALUES (		1, '/static/images/gift_box.png', 'http://www.dog.com', 'dog house', 'Hand made dog house' , 1078.0);
	INSERT INTO tbl_products VALUES (		2, '/static/images/gift_box.png', 'http://www.cat.com', 'a tabby cat', 'get me 3 cats from RSPCA', 234.0);
	INSERT INTO tbl_products VALUES (		3, '/static/images/gift_box.png', 'http://www.tshirts.com', 'A green t-shirt', 'I need a new T-Shirt. pref green.', 2.0);
	INSERT INTO tbl_products VALUES (		4, '/static/images/gift_box.png', 'http://www.bikes.com', 'A bike.', 'Need a new bike. :}', 437.0);
	INSERT INTO tbl_products VALUES (		5, '/static/images/gift_box.png', 'http://www.toyota.com', 'Toyota 86', 'Toyota 86 pls!!!!', 90.0);
	INSERT INTO tbl_products VALUES (		6, '/static/images/gift_box.png', 'http://www.iloveguavas.com', 'A guava', 'guavas are the best', 12.0);
	INSERT INTO tbl_products VALUES (		7, '/static/images/gift_box.png', 'http://www.apple.com', 'iTunes gift card', 'Need more music.', 2042114.0);
	INSERT INTO tbl_products VALUES (		8, '/static/images/gift_box.png', 'http://www.socks.com', 'socks', 'I actually need socks :{', 8098.0);
	INSERT INTO tbl_products VALUES (		9, '/static/images/gift_box.png', 'http://www.shoes.com', 'Shoes', 'I got 99 socks but a shoe aint one', 12242.0);
	INSERT INTO tbl_products VALUES (		10, '/static/images/gift_box.png', 'http://www.raspberryPI.com', 'A raspberry PI', 'A raspberry PI would be rad!', 123.0);
	INSERT INTO tbl_products VALUES (		11, '/static/images/gift_box.png', 'http://www.google.com', 'A nexus 5', 'Great phone 10/10 pls buy', 3563.0);
	INSERT INTO tbl_products VALUES (		12, '/static/images/gift_box.png', 'http://www.iloveguavas.com', 'A guava', 'guavas are the best', 331.0);
	INSERT INTO tbl_products VALUES (		13, '/static/images/gift_box.png', 'http://www.apple.com', 'iTunes gift card', 'Need more music.', 875.0);
	INSERT INTO tbl_products VALUES (		14, '/static/images/gift_box.png', 'http://www.socks.com', 'socks are cool', 'I actually need socks :{', 21.0);
	INSERT INTO tbl_products VALUES (		15, '/static/images/gift_box.png', 'http://www.shoes.com', 'Shoes', 'I got 99 socks but a shoe aint one', 9874.0);
	INSERT INTO tbl_products VALUES (		16, '/static/images/gift_box.png', 'http://www.raspberryPI.com', 'A raspberry PI', 'A raspberry PI would be rad!', 122.0);
	INSERT INTO tbl_products VALUES (		17, '/static/images/gift_box.png', 'http://www.google.com', 'A nexus 5', 'Great phone 10/10 pls buy', 6323.0);
	INSERT INTO tbl_products VALUES (		18, '/static/images/gift_box.png', 'http://www.iloveguavas.com', 'A guava', 'guavas are the best', 853.0);
	INSERT INTO tbl_products VALUES (		19, '/static/images/gift_box.png', 'http://www.apple.com', 'iTunes gift card', 'Need more music.', 421.0);
	INSERT INTO tbl_products VALUES (		20, '/static/images/gift_box.png', 'http://www.socks.com', 'socks', 'I actually need socks :{', 245322.0);
	INSERT INTO tbl_products VALUES (		21, '/static/images/gift_box.png', 'http://www.shoes.com', 'Shoes', 'I got 99 socks but a shoe aint one', 3565.0);
	INSERT INTO tbl_products VALUES (		22, '/static/images/gift_box.png', 'http://www.raspberryPI.com', 'A raspberry PI', 'A raspberry PI would be rad!', 34535.0);
	INSERT INTO tbl_products VALUES (		23, '/static/images/gift_box.png', 'http://www.google.com', 'A nexus 5', 'Great phone 10/10 pls buy', 34534.0);

	INSERT	INTO tbl_wish_list	VALUES	(10, 'birthday', 9 );
	INSERT	INTO tbl_wish_list	VALUES (11, 'Christmas', 1 );
	INSERT	INTO tbl_wish_list	VALUES (12, 'Easter', 0 );
	INSERT	INTO tbl_wish_list	VALUES (13, 'Thanksgiving', 2 );
	INSERT	INTO tbl_wish_list	VALUES (14, 'Halloween', 3 );

	INSERT INTO tbl_list_item VALUES (	10, 1, 0);
	INSERT INTO tbl_list_item VALUES (	 10 , 2, 0 );
	INSERT INTO tbl_list_item VALUES (	 10 , 23,0);
	INSERT INTO tbl_list_item VALUES (	 10 , 3, 0 );
	INSERT INTO tbl_list_item VALUES (	11, 1, 0);
	INSERT INTO tbl_list_item VALUES (	 11 , 7, 0 );
	INSERT INTO tbl_list_item VALUES (	 11 , 3,0);
	INSERT INTO tbl_list_item VALUES (	 11 , 6, 0 );
	INSERT INTO tbl_list_item VALUES (	11, 21, 0);
	INSERT INTO tbl_list_item VALUES (	 12 , 7, 0 );
	INSERT INTO tbl_list_item VALUES (	 12 , 10,0);
	INSERT INTO tbl_list_item VALUES (	 12 , 19, 0 );
	INSERT INTO tbl_list_item VALUES (	12, 13, 0);
	INSERT INTO tbl_list_item VALUES (	 12 , 8, 0 );
	INSERT INTO tbl_list_item VALUES (	13, 4, 0);
	INSERT INTO tbl_list_item VALUES (	 13 , 3, 0 );
	INSERT INTO tbl_list_item VALUES (	14, 4, 0);
	INSERT INTO tbl_list_item VALUES (	 14 , 14, 0 );
	INSERT INTO tbl_list_item VALUES (	14, 17, 0);
	INSERT INTO tbl_list_item VALUES (	 14 , 11, 0 );

	INSERT INTO tbl_friends VALUES (9,0) ;
	INSERT INTO tbl_friends VALUES (0,9) ;
	INSERT INTO tbl_friends VALUES (9,1) ;
	INSERT INTO tbl_friends VALUES (1, 9) ;
	INSERT INTO tbl_friends VALUES (2, 9) ;
	INSERT INTO tbl_friends VALUES (9,2) ;
	INSERT INTO tbl_friends VALUES (9,3) ;
	INSERT INTO tbl_friends VALUES (3,9) ;
	'''

	conn = sqlite3.connect("wishlist.db")
	conn.executescript(sqlscript)
	conn.commit()

	#populate users
	names = []
	emails = []
	usernames = []
	passwords = []

	with open("random_names.txt") as n:
		for j in n:
			j = j.rstrip()
			names.append(j)

	for i in names:
		email = i + str(randint(0,10)) + str(randint(0,10)) +str(randint(0,10)) +str(randint(0,10)) +"@.yoloteamfour.com"
		emails.append(email)
		username = i[:randint(2,4)] + str(randint(0,10))
		usernames.append(username)
		password = i[::-1]
		passwords.append(password)

	i = 0
	while i < len(emails):
		random_num = randint(0, len(names) -1 )
		fname_index = names[randint(0,len(names) - 1)]
		lname_index = names[randint(0,len(names) - 1)]
		username_index = usernames[random_num]
		email_index = emails[random_num]
		password_index = passwords[random_num]
		generate_user_row(conn, fname_index, lname_index, username_index, email_index, password_index, str(randint(1900,2000)) + "-" + str(randint(0, 12)) + "-" + str(randint(0, 31)))
		i += 1

	conn.commit()
	conn.close()

if __name__ == "__main__":
	initdb()
	#import cProfile
	#print(cProfile.run("initdb()"))
