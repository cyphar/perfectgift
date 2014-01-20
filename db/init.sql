-- Used to create a new wishlist database
-- NOTE: run clean.sql *before* running this.

CREATE TABLE tbl_users (
	user_id INTEGER NOT NULL ,
	fname TEXT NOT NULL,
	lname TEXT NOT NULL,
	username TEXT NOT NULL UNIQUE,
	email TEXT NOT NULL UNIQUE,
	image TEXT NOT NULL,
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
