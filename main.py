
import psycopg2
import streamlit as st

import toml
from dbcontrol import password_validation, password_hash

placeholder = st.empty()
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

    if user:
        password = user[4]
        if password_validation(passwrd, bytes(password)):
            return True
    return False
def user_profile(username):
    query = f"SELECT * FROM userinfo WHERE username='{username}';"
    curr.execute(query)
    user = curr.fetchone()
    username =user[1]
    email =user[2]
    ages =user[3]
    password =user[4]
    firstname =user[5]
    lastname =user[6]
    allergy =user[7]
    dietary =user[8]


def user_add(username, password, email, age, firstname, lastname ,allergy ,dietary):
    hashed_pass = password_hash(password)
    query = f"INSERT INTO userinfo(username,email,ages,password,firstname,lastname,allergy,dietary) VALUES ({username}','{email}','{age}','{hashed_pass}','{firstname}','{lastname}','{allergy}','{dietary}')"
    curr.execute(query)
    conn.commit()


def login():


    st.markdown(f"""
    <style>
    .stApp {{
    background-image: url("https://images.pexels.com/photos/1640773/pexels-photo-1640773.jpeg");
    background-size: 100vw 100vh;
    background-position: center; 
    background-repeat: no-repeat;}}
    </style>
    """, unsafe_allow_html=True)
    with placeholder.container():
        title = '<span style="font-size:30px;">:red[Welcome to:**COOKBUDDY**]</span>'
        st.markdown(title, unsafe_allow_html=True)
        sbox = st.selectbox(':red[**Login/Sign Up**]', ['Login', 'Sign Up'])
        if sbox == 'Login':
            st.markdown(":red[**Login**]")
            username = st.text_input(':red[**Username**]', placeholder='Enter your username')
            password = st.text_input(':red[**Password**]', placeholder='Enter your password', type='password')
            if st.button('Login'):
                if user_control(username, password):
                    placeholder.empty()
                else:
                    st.error("Check your username and password")
        if sbox == 'Sign Up':
            st.markdown(":red[**Sign Up**]")
            username = st.text_input(':red[**Username**]', placeholder='Enter your username')
            password = st.text_input(':red[**Password**]', placeholder='Enter your password', type='password')
            email = st.text_input(':red[**Email**]', placeholder='Enter your email')
            age = st.text_input(':red[**Age**]', placeholder='Enter your age')
            firstname = st.text_input(':red[**Firstname**]', placeholder='Enter your firstname')
            lastname = st.text_input(':red[**Lastname**]', placeholder='Enter your lastname')
            allergy = st.text_input(':red[**Allergy**]', placeholder='Do you have any allergies? If so, what are they?')
            dietary = st.text_input(':red[**Dietary**]', placeholder='Do you have a special diet, such as being a vegetarian?')
            if st.button('Sign Up'):
                user_add(username, password, email, age, firstname, lastname ,allergy ,dietary)


if __name__ == "__main__":
    login()
