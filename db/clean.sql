-- Cleans an existing wishlist database
-- NOTE: Run this *before* running init.sql

DROP TABLE IF EXISTS tbl_users;
DROP TABLE IF EXISTS tbl_products;
DROP TABLE IF EXISTS tbl_friends;
DROP TABLE IF EXISTS tbl_wish_list;
DROP TABLE IF EXISTS tbl_list_item;
