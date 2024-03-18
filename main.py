import psycopg2
import streamlit as st

import toml
from dbcontrol import password_validation, password_hash

secrets = toml.load("secrets.toml")
postgres = secrets["postgres"]
try:
    conn = psycopg2.connect(
        database=postgres["database"],
        user=postgres["user"],
        host=postgres["host"],
        port=postgres["port"],
        password=postgres["password"]
    )
except Exception as e:
    st.error(f"Error database connection{e}")
curr = conn.cursor()


def user_control(username, passwrd):
    query = f"SELECT * FROM userinfo WHERE username='{username}';"
    curr.execute(query)
    user = curr.fetchone()
    curr.close()
    if user:
        password = user[4]
        if password_validation(passwrd, bytes(password)):
            return True
    return False


def user_add(username, password, email, age, firstname, lastname):
    hashed_pass = password_hash(password)
    query = f"INSERT INTO userinfo(username,password,email,ages,firstname,lastname) VALUES ('{username}','{password}','{email}','{age}','{firstname}','{lastname}')"
    curr.execute(query)
    conn.commit()


def login():
    title = '<span style="font-size:30px;">Welcome to:**COOKBUDDY**</span>'
    st.markdown(title, unsafe_allow_html=True)
    sbox = st.selectbox('Login/Sign Up', ['Login', 'Sign Up'])
    if sbox == 'Login':
        st.markdown("**LOGIN**")
        username = st.text_input('Username', placeholder='Enter your username')
        password = st.text_input('Password', placeholder='Enter your password', type='password')
        if st.button('Login'):
            if user_control(username, password):
                st.success("logged")
            else:
                st.error("error")
    if sbox == 'Sign Up':
        st.markdown("**Sign Up**")
        username = st.text_input('Username', placeholder='Enter your username')
        password = st.text_input('Password', placeholder='Enter your password', type='password')
        email = st.text_input('Email', placeholder='Enter your email')
        age = st.text_input('Age', placeholder='Enter your age')
        firstname = st.text_input('Firstname', placeholder='Enter your firstname')
        lastname = st.text_input('Lastname', placeholder='Enter your lastname')
        if st.button('Sign Up'):
            user_add(username, password, email, age, firstname, lastname)


if __name__ == "__main__":
    login()
