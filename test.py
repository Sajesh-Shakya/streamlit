import streamlit as st
import numpy as np
import time
import yfinance as yf
import streamlit_authenticator as stauth
from datetime import datetime
import database as db #bring all the functions from database into the app



# create session state variables which exist outside page re runs
# use if not in session state so it is not overwritten in re runs 

# see if logged in or not
if "authentication_status" not in st.session_state:
    st.session_state['authentication_status'] = None


# define the sidebar
side = st.sidebar

log_sign = side.selectbox("login/signup", ["login", "register"])
    



if log_sign == "login":
    #LOGIN
    users = db.fetch_all_users()
    # retrieves database as dictionaries

    # make each field in db a list
    username = [x["key"] for x in users]
    name = [x["name"] for x in users]
    hashed = [x["password"] for x in users]

    credentials = {"usernames":{}} #{username:{username[0]:{name:name[0], password:password[0]}}}  
    for name,un,pw in zip(name, username, hashed):
        user_dict = {"name":name, "password":pw}
        credentials["usernames"].update({un:user_dict})

    authenticator = stauth.Authenticate(credentials,cookie_name="test",key= "abc",cookie_expiry_days=1) 
    name, status, username = authenticator.login("Login", "sidebar")

    # conditions based on status


if log_sign == "register":
    register_user_form = st.sidebar.form('Register user') # create form object

    register_user_form.subheader("Registration")
    username = register_user_form.text_input('Username').lower()
    name = register_user_form.text_input('Name')
    password = register_user_form.text_input('Password', type='password')
    password_repeat = register_user_form.text_input('Repeat password', type='password')
    # validation
    if register_user_form.form_submit_button('Register'):
        if len(username) and len(name) and len(password) and len(password_repeat)> 0:
            if db.get_user(username) == None:
                if len(password) > 9 and len(password_repeat) > 9:
                    if password == password_repeat:
                        if name.isalpha():
                            db.add_user(username, name, password) # add user
                            register_user_form.write("Successlfully created new account, Now please log in")
                        else:
                            register_user_form.error("name must only contain letters")
                    else:
                        register_user_form.error('Passwords do not match')
                else:
                    register_user_form.error('Password must be at least 10 characters long')
            else:
                register_user_form.error('Username already taken')
        else:
            register_user_form.error('Please enter a username, name, and password')


if st.session_state['authentication_status'] == False:
    st.sidebar.error("Wrong username or password")
    st.write("""
             # Login on the start page to view this page
             """)
if st.session_state['authentication_status'] == None:
    st.sidebar.error("enter your details")
    st.write("""
             # Login on the start page to view this page
             """)
if st.session_state['authentication_status']:
    authenticator.logout("Logout" , "sidebar")
    #APP
    st.write("""
    # Account

    """)
    

    st.subheader("Hello "+str(username))
    st.subheader("User details")
    
    

    st.write("""
        # reset password form
        """)
    reset = st.form("Reset Password") # reset password form

    
    current_pw = reset.text_input('Current password')
    new_pw = reset.text_input('Password', type='password')
    repeat_pw = reset.text_input('Repeat password', type='password')
    
    #boolean value for if current password match with database password
    check = db.pw_check(username, current_pw)

    if reset.form_submit_button('Reset password'):
        if check:
            if len(current_pw) and len(new_pw) and len(repeat_pw) > 0:
                if current_pw != new_pw:
                    if new_pw == repeat_pw:
                        hashed = stauth.Hasher([new_pw]).generate()[0]
                        db.update_user(st.session_state.username,{"password":hashed})
                        reset.success("Password has been reset")
                    else:
                        reset.error('Passwords do not match')
                else:
                    reset.error('You have not changed the password')
            else:
                reset.error('Please enter an email, username, name, and password')
        else:
            reset.error("Incorrect Password")
           

    st.write("""
            ## update password
            """)
    update = st.form("update user details") # reset password form
    field = update.selectbox("field", ["username", "name"])
    mess = "type new detail"
    detail= update.text_input(mess)    

    if update.form_submit_button('Update detail'):
        if len(detail) > 0:
            if field == "username":
                db.update_user(st.session_state.username,{"key":detail})
                update.success("username updated")
            if field == "name":
                db.update_user(st.session_state.username,{"name":detail})
                update.success("name updated")
        else:
            update.error("please enter something")

            
    
#st.slider()
#tickerData.history()
#datetime()