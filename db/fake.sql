-- Fake data for the wishlist database.
-- NOTE: USED FOR TESTING.

INSERT INTO tbl_users (rowid, fname, lname, username, email, image, password, salt, dob) VALUES (0, 'Barry', 'Schultz', 'bazS', 'bazS@here.now', "0.jpg", '3a3b2372dd1f0c0f5e8bdd3196bb29dbcbd7f75a55abb9ba9ab2f60243bcd517', "x_HCV[`/", 859816800);
INSERT INTO tbl_users (rowid, fname, lname, username, email, image, password, salt, dob) VALUES (1, 'Prue', 'Robinson', 'pruR', 'pruR@here.now', "1.jpg", 'f19ac3fa320b096735b4f734aba6550734213a35c28bdcec4eed5a78157daf14', "y{DZp?uc", 859816800);
INSERT INTO tbl_users (rowid, fname, lname, username, email, image, password, salt, dob) VALUES (2, 'Andrew', 'Varvel', 'andV', 'andV@here.now', "2.jpg", 'e5aabf82efd3ea15d803e2190a18e3131b22c2f013dcf8a9d600b5f06cd0242d', "(cFg^KtE", 859816800);
INSERT INTO tbl_users (rowid, fname, lname, username, email, image, password, salt, dob) VALUES (3, 'Mathew', 'Nemes', 'matN', 'matN@here.now', "3.jpg", '05acaabdba3907e829b330f81c8b3deace38ccbefa1ef795534107d15eee95e1', "i]xs@K\\W", 859816800);
INSERT INTO tbl_users (rowid, fname, lname, username, email, image, password, salt, dob) VALUES (4, 'Mara', 'Barber', 'marB', 'marB@here.now', "4.jpg", '307f8f39111c1988983953b24a343e91222df1edccfd95e809b31268cf1f54a4', "VoAqaR1i", 859816800);
INSERT INTO tbl_users (rowid, fname, lname, username, email, image, password, salt, dob) VALUES (5, 'Scott', 'Herdman', 'scoH', 'scoH@here.now', "5.jpg", '0f6d189941215610b505b9354d47ae33431e00546ba9f4afc92b39f9c381e4fc', "E-G,M%UZ", 859816800);
INSERT INTO tbl_users (rowid, fname, lname, username, email, image, password, salt, dob) VALUES (6, 'Alec', 'Newton', 'aleN', 'aleN@here.now', "6.jpg", '8f71b161b562d7c0d3b01babcd454cbd4b9319b8b92a1d555dde614a79a29e23', "SVe>88P.", 859816800);
INSERT INTO tbl_users (rowid, fname, lname, username, email, image, password, salt, dob) VALUES (7, 'Karen', 'Barber', 'karB', 'karB@here.now', "7.jpg", '052b43fd7391614896cb2cf37eae4a0fb514a25b55731809a169fd0e72ccb84c', ", 5&ud,[q", 859816800);
INSERT INTO tbl_users (rowid, fname, lname, username, email, image, password, salt, dob) VALUES (8, 'Grant', 'Ovzinsky', 'granO', 'granO@here.now', "8.jpg", '1c9fe0f03bfd50c9df89a42e27f7041606d8c8b49e102e645628c57ef5ea2d25', "ev\\0Qqb2", 859816800);
INSERT INTO tbl_users (rowid, fname, lname, username, email, image, password, salt, dob) VALUES (9, 'Nick', 'Wright', 'admin', 'admin@group4.com', "9.jpg", 'd86a0c720b776de00005283374c17fa3243094d2aa482db36f6311bc801e9f2f', 'z(z6|Z3Q', 859816800);

INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (0, 'smiley pillow', '/static/images/gift_box.png', 'http://www.smiley.com', 'cutesy smiley pillow at MYER', 2014.0 );
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (1, 'dog house', '/static/images/gift_box.png', 'http://www.dog.com', 'Hand made dog house' , 1078.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (2, 'a tabby cat', '/static/images/gift_box.png', 'http://www.cat.com', 'get me 3 cats from RSPCA', 234.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (3, 'A green t-shirt', '/static/images/gift_box.png', 'http://www.tshirts.com', 'I need a new T-Shirt. pref green.', 2.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (4, 'A bike.', '/static/images/gift_box.png', 'http://www.bikes.com', 'Need a new bike. :}', 437.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (5, 'Toyota 86', '/static/images/gift_box.png', 'http://www.toyota.com', 'Toyota 86 pls!!!!', 90.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (6, 'A guava', '/static/images/gift_box.png', 'http://www.iloveguavas.com', 'guavas are the best', 12.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (7, 'iTunes gift card', '/static/images/gift_box.png', 'http://www.apple.com', 'Need more music.', 2042114.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (8, 'socks', '/static/images/gift_box.png', 'http://www.socks.com', 'I actually need socks :{', 8098.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (9, 'Shoes', '/static/images/gift_box.png', 'http://www.shoes.com', 'I got 99 socks but a shoe aint one', 12242.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (10, 'A raspberry PI', '/static/images/gift_box.png', 'http://www.raspberryPI.com', 'A raspberry PI would be rad!', 123.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (11, 'A nexus 5', '/static/images/gift_box.png', 'http://www.google.com', 'Great phone 10/10 pls buy', 3563.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (12, 'A guava', '/static/images/gift_box.png', 'http://www.iloveguavas.com', 'guavas are the best', 331.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (13, 'iTunes gift card', '/static/images/gift_box.png', 'http://www.apple.com', 'Need more music.', 875.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (14, 'socks are cool', '/static/images/gift_box.png', 'http://www.socks.com', 'I actually need socks :{', 21.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (15, 'Shoes', '/static/images/gift_box.png', 'http://www.shoes.com', 'I got 99 socks but a shoe aint one', 9874.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (16, 'A raspberry PI', '/static/images/gift_box.png', 'http://www.raspberryPI.com', 'A raspberry PI would be rad!', 122.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (17, 'A nexus 5', '/static/images/gift_box.png', 'http://www.google.com', 'Great phone 10/10 pls buy', 6323.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (18, 'A guava', '/static/images/gift_box.png', 'http://www.iloveguavas.com', 'guavas are the best', 853.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (19, 'iTunes gift card', '/static/images/gift_box.png', 'http://www.apple.com', 'Need more music.', 421.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (20, 'socks', '/static/images/gift_box.png', 'http://www.socks.com', 'I actually need socks :{', 245322.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (21, 'Shoes', '/static/images/gift_box.png', 'http://www.shoes.com', 'I got 99 socks but a shoe aint one', 3565.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (22, 'A raspberry PI', '/static/images/gift_box.png', 'http://www.raspberryPI.com', 'A raspberry PI would be rad!', 34535.0);
INSERT INTO tbl_products (rowid, name, image, link, description, price) VALUES (23, 'A nexus 5', '/static/images/gift_box.png', 'http://www.google.com', 'Great phone 10/10 pls buy', 34534.0);

INSERT INTO tbl_wish_list (wish_id, list_name, user_id) VALUES (10, 'Birthday', 9);
INSERT INTO tbl_wish_list (wish_id, list_name, user_id) VALUES (11, 'Christmas', 1);
INSERT INTO tbl_wish_list (wish_id, list_name, user_id) VALUES (12, 'Easter', 0);
INSERT INTO tbl_wish_list (wish_id, list_name, user_id) VALUES (13, 'Thanksgiving', 2);
INSERT INTO tbl_wish_list (wish_id, list_name, user_id) VALUES (14, 'Halloween', 3);

INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (10, 1, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (10, 2, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (10, 23, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (10, 3, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (11, 1, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (11, 7, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (11, 3, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (11, 6, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (11, 21, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (12, 7, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (12, 10, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (12, 19, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (12, 13, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (12, 8, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (13, 4, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (13, 3, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (14, 4, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (14, 14, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (14, 17, 0);
INSERT INTO tbl_list_item (list_id, product_id, checked) VALUES (14, 11, 0);

INSERT INTO tbl_friends (f_user_id, friend_id) VALUES (9, 0);
INSERT INTO tbl_friends (f_user_id, friend_id) VALUES (0, 9);
INSERT INTO tbl_friends (f_user_id, friend_id) VALUES (9, 1);
INSERT INTO tbl_friends (f_user_id, friend_id) VALUES (1, 9);
INSERT INTO tbl_friends (f_user_id, friend_id) VALUES (2, 9);
INSERT INTO tbl_friends (f_user_id, friend_id) VALUES (9, 2);
INSERT INTO tbl_friends (f_user_id, friend_id) VALUES (9, 3);
INSERT INTO tbl_friends (f_user_id, friend_id) VALUES (3, 9);
