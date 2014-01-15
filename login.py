from tornado.ncss import Server
from password import passCheck, hashPw, saltGen
import epyc
from DBAPI import User, UserNotFound
import re

# decorator function for checking that the user is logged in
def logged_in(fn):
    def inner(response, *args, **kwargs):
        userid = response.get_secure_cookie('userid')
        # if logged in then do function
        if userid is not None:
            return fn(response, *args, **kwargs)
        # if NOT logged in then display login page
        return response.redirect('/login')
    return inner
    
def get_current_user(response):
    userid = response.get_secure_cookie('userid')
    if userid:
        userid = userid.decode("utf-8")
    else:
        userid = False
    return userid
    
@logged_in
def is_current_users_wishlist_page(response, username):
    if get_current_user(response) == username:
        return True
    return False
        
        
#commented out as we don't want landing page to be login page
#def home(response):
#    if response.get_secure_cookie('userid') is None:
#        response.redirect('/login')
#    else:
#        response.write('hello world')

@logged_in
def hello(response):
    response.write('''
    <html>
    <header>:)</header>
    <body>
    <h1>Hellos peoples of the internets</h1>
    </body>
    </html>
''')

def login(response):
    uid=response.get_field("uid")
    pwd=response.get_field("pwd", strip=False)
    userid=response.get_secure_cookie('userid')
    
    if uid == '' or pwd == '':
        response.write(epyc.render("templates/login.html", {"error": "Login failed, check username and password", "logged_in": get_current_user(response)}) )
        print("failed login")
    elif uid and pwd:
        if User.check_password(uid, pwd):
            response.set_secure_cookie('userid', uid)
            print("login:"+str(uid))
            response.redirect('/users/'+str(uid))
        else:
            scope = {"error": "Incorrect username or password.", "logged_in": get_current_user(response)}
            response.write(epyc.render("templates/login.html", scope))
            print("failed login")
    elif userid:
        response.redirect('/users/'+ userid.decode('utf-8'))
    else:
        response.write(epyc.render("templates/login.html",{"logged_in":get_current_user(response)}))

def logout(response):
    response.clear_cookie("userid")
    response.redirect('/')

##    userid=response.get_secure_cookie('userid')
##    if userid is None:
##        response.redirect('/login')
##    else:
##        response.clear_cookie('userid')
##        response.redirect('/login')
##class User:
##    def __init__(self, user, password):
##        self.user=user
##        self.password=password
##    def pas(self):
##        pas=self.password
##    def user(self):
##        user=self.user
##    def login(user,pas):
##        if user in users and pas in passw:
##            return True

  
def signup(response):
    fname=response.get_field("fname")
    lname=response.get_field("lname")
    email=response.get_field("email")
    username=response.get_field("username")
    password=response.get_field("password")
    # response.redirect('/login')
    # check for invalid input
    if not fname:   
        response.write(epyc.render("templates/login.html", {"error": "Create account failed, first name required", \
                                                            "logged_in": get_current_user(response), "fname": fname, \
                                                            "lname": lname, "email": email, "username": username}) )
    elif not lname:
        response.write(epyc.render("templates/login.html", {"error": "Create account failed, last name required", \
                                                            "logged_in": get_current_user(response), "fname": fname, \
                                                            "lname": lname, "email": email, "username": username}) )
    elif not re.match("^[-a-zA-Z0-9\+\._]+@([-a-zA-Z0-9]+\.)+[a-zA-Z]+$",email):
        response.write(epyc.render("templates/login.html", {"error": "Create account failed, valid email address required", \
                                                            "logged_in": get_current_user(response), "fname": fname, \
                                                            "lname": lname, "email": email, "username": username}) )
    elif not re.match("^[a-zA-Z0-9_]+$", username):
        response.write(epyc.render("templates/login.html", {"error": "Create account failed, username must contain letters, numbers or underscore only", \
                                                            "logged_in": get_current_user(response), "fname": fname, \
                                                            "lname": lname, "email": email, "username": username}) )
    elif len(password) < 6:
        response.write(epyc.render("templates/login.html", {"error": "Create account failed, password is too short", \
                                                            "logged_in": get_current_user(response), "fname": fname, \
                                                            "lname": lname, "email": email, "username": username}) )
    else: #at testing passed all requirements
        try: 
            User.find_user(username)
            response.write(epyc.render("templates/login.html", {"error": "Create account failed, username already in use", \
                                                                "logged_in": get_current_user(response)}) )
        except UserNotFound:
            u = User.create_user(fname,lname,username,email,password)
            u.create_wish_list(str(username)+"'s wishlist")
            response.set_secure_cookie('userid',username)
            response.redirect('/users/' + u.username)
if __name__ == '__main__':
    server=Server()
    #server.register('/home',home)
    server.register('/', hello)
    server.register('/login', login)
    server.register('/logout', logout)
    server.register('/signup',signup)
    server.run()