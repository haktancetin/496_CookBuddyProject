import streamlit as st


st.markdown(f"""
    <style>
    .stApp {{
    background-image: url("https://images.pexels.com/photos/1640773/pexels-photo-1640773.jpeg");
    background-size: 100vw 100vh;
    background-position: center; 
    background-repeat: no-repeat;}}
    </style>
    """, unsafe_allow_html=True)
with st.form("**Profile**"):
    username = st.text_input(':red[**Username**]')
    password = st.text_input(':red[**Password**]',  type='password')
    email = st.text_input(':red[**Email**]')
    age = st.text_input(':red[**Age**]')
    firstname = st.text_input(':red[**Firstname**]')
    lastname = st.text_input(':red[**Lastname**]')
    allergy = st.text_input(':red[**Allergy**]')
    dietary = st.text_input(':red[**Dietary**]')
    st.form_submit_button("Save")
