from deta import Deta
import streamlit_authenticator as stauth
import bcrypt

DATA_KEY = "a0uuaqpadph_814U6zmCSKsFucT3uXU2s6rz86gb8BHL"

#initilize Deta object using the KEY
deta = Deta(DATA_KEY)

#name the database
db = deta.Base("stream_login")

#define some functions

def add_user(username,name, password):
    #primary key = username, same username => old entry overwritten
    # initially was 
        #hashed = stauth.Hasher(password).generate() # returns list 
        #db.put({"key":username,"name":name,"password":hashed[0]})

    if db.get(username) == None: #add a conditional statement so usernames are not overwritten
        salt = bcrypt.gensalt()# create a salt
        hashed = bcrypt.hashpw(password.encode(), salt).decode()# goes from a binary string to normal string
        db.put({"key":username,"name":name,"password":hashed})# add to database
    else:
        return -1 # to show there was an error in executiobn

add_user("q","c","1")
add_user("v","e","13")
add_user("p","z","2")

def get_user(username):
    #if not username returns None
    return db.get(username)
    

def fetch_all_users():
    res = db.fetch()
    return res.items # returns ditionary of contents in the database

def update_user(username, update):
    #enter update as a dictionary
    db.update(update, username)

def delete_user(username):
    db.delete()
    #deletes record for record wih user name

def pw_check(username, pw):
    x = bcrypt.checkpw(pw.encode(), get_user(username)["password"].encode()) # checks the password
    return x 

#print(get_user("q"))
#pw = "1"

#h = pw.encode() # encode entered password and hashed password
#x = bcrypt.checkpw(h, get_user("q")["password"].encode()) # checks the password
#print(x)

#print(pw_check("q", "2"))
