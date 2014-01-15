
import re

names = []
emails = []
usernames = []

#Add data to lists
#names
with open("random_names.txt") as n:
	for j in n:
		names.append(j)

#emails
for i in names:
	email = i + "@.yoloteamfour.com"
	emails.append(email)

#usernames 
for i in names:
	username = i[:randint(2,4)] + str(randint(0,10))
	usernames.append(username)


print(names)
print(emails)
print(usernames)