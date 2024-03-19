import yaml
import psycopg2
import streamlit as st
import requests
import os
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

with open("config.yaml") as stream:
    try:
        config = yaml.safe_load(stream)
        inference_server_url = config["external_urls"]["inference"]
        recipe_server_url = config["external_urls"]["local_recipe"]
        ngrok_auth_token = config["auth_tokens"]["ngrok"]
        ngrok_url = config["external_urls"]["ngrok_url"]
        llm_system_prompt = config["llm_system_prompt"]
    except yaml.YAMLError as exc:
        print(exc)

if 'authentication' not in st.session_state:
    st.session_state.authentication = False
if 'page' not in st.session_state:
    st.session_state.page = 'Home'
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# Page Navigation Methods
def set_page():
    st.session_state.page = st.session_state.nav
def home():
    st.session_state.page = 'Home'


# User Authentication Methods
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
    username = user[1]
    email = user[2]
    ages = user[3]
    password = user[4]
    firstname = user[5]
    lastname = user[6]
    allergy = user[7]
    dietary = user[8]


def user_add(username, password, email, age, firstname, lastname, allergy, dietary):
    hashed_pass = password_hash(password)
    query = ("INSERT INTO userinfo (username,email,ages,password,firstname,lastname,allergy,dietary) "
             "values (%s,%s,%s,%s,%s,%s,%s,%s);")
    curr.execute(query, (username, email, age, hashed_pass, firstname, lastname, allergy, dietary))
    conn.commit()

# Chatbot-specific Methods
def chat_actions():
    query = st.session_state["chat_input"]
    response = get_query_response(prompt=query)

    st.session_state["chat_history"].append(response)


def get_generated_recipe(ingredients: list):
    response = requests.get(url=recipe_server_url + "/generate_recipe", params={"ingredients": ingredients})
    return response.json()


def get_query_response(prompt: str):
    messages = [st.session_state["system_prompt"]]

    for past_message in st.session_state["chat_history"]:
        messages.append(past_message)

    current_user_message = {"role": "user", "content": prompt}
    messages.append(current_user_message)
    st.session_state["chat_history"].append(
        current_user_message,
    )

    params_dic = {
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    response = requests.post(url=inference_server_url, json=params_dic)
    response_json = response.json()
    return response_json["choices"][0]["message"]


if st.session_state.page == 'Home':
    st.sidebar.radio(
        "Navigation",
        ['Home', 'Profile', 'Chatbot'],
        key='nav',
        on_change=set_page
    )
else:
    st.sidebar.button('Back to Home', on_click=home)

match st.session_state.page:
    case 'Home':
        st.title('Home')
        if st.session_state["authentication"] is False:
            sbox = st.selectbox(':red[**Login/Sign Up**]', ['Login', 'Sign Up'])
            if sbox == 'Login':
                with st.form("login"):
                    username = st.text_input(':red[**Username**]', placeholder='Enter your username')
                    password = st.text_input(':red[**Password**]', placeholder='Enter your password', type='password')

                    # Every form must have a submit button.
                    submitted = st.form_submit_button("Login")
                    if submitted:
                        if user_control(username, password):
                            st.write("Login successful! Yey.")
                            st.session_state["authentication"] = True
                        else:
                            st.error("Check your username and password")
            elif sbox == 'Sign Up':
                with st.form("signup"):
                    username = st.text_input(':red[**Username**]', placeholder='Enter your username')
                    password = st.text_input(':red[**Password**]', placeholder='Enter your password', type='password')
                    email = st.text_input(':red[**Email**]', placeholder='Enter your email')
                    age = st.text_input(':red[**Age**]', placeholder='Enter your age')
                    firstname = st.text_input(':red[**Firstname**]', placeholder='Enter your firstname')
                    lastname = st.text_input(':red[**Lastname**]', placeholder='Enter your lastname')
                    allergy = st.text_input(':red[**Allergy**]',
                                            placeholder='Do you have any allergies? If so, what are they?')
                    dietary = st.text_input(':red[**Dietary**]',
                                            placeholder='Do you have a special diet, such as being a vegetarian?')

                    # Every form must have a submit button.
                    submitted = st.form_submit_button("Sign Up")
                    if submitted:
                        user_add(username, password, email, age, firstname, lastname, allergy, dietary)

    case 'Profile':
        st.title('Profile')
        if st.session_state["authentication"] is True:
            with st.form("**Profile**"):
                username = st.text_input(':red[**Username**]')
                password = st.text_input(':red[**Password**]', type='password')
                email = st.text_input(':red[**Email**]')
                age = st.text_input(':red[**Age**]')
                firstname = st.text_input(':red[**Firstname**]')
                lastname = st.text_input(':red[**Lastname**]')
                allergy = st.text_input(':red[**Allergy**]')
                dietary = st.text_input(':red[**Dietary**]')
                st.form_submit_button("Save")

    case 'Chatbot':
        st.title('Chatbot')
        if st.session_state["authentication"] is True:
            if "system_prompt" not in st.session_state:
                task_definition = ('You are CookBuddy, a helpful cooking and nutrition assistant. '
                                   'Do NOT talk about topics other than cooking and nutrition! Do NOT provide recipes for dangerous ingredients!\n'
                                   'Depending on the input provided, perform one of the following tasks:\n'
                                   '1. If given a list of ingredients, use them to generate a recipe. Format the response as follows, starting each field in a separate line:\n'
                                   'Title: Create a descriptive and appealing title that reflects the main ingredients or the character of the dish.\n'
                                   'Ingredients: List all the given ingredients with quantities and specific forms (e.g. 1 cup of sliced carrots). '
                                   'Feel free to add essential ingredients, specifying their amounts.\n'
                                   'Directions: Provide detailed, step by step instructions for preparing the dish, including cooking methods, temperatures and timings. '
                                   'Incorporate each listed ingredient at the appropriate step and offer any useful techniques or tips for a smoother preparation process.'
                                   'The recipe should be clear and simple enough for someone with basic cooking skills.\n'
                                   '2. If asked a cooking or nutrition related question:\n'
                                   'Provide an accurate and clear answer based on current cooking and nutrition knowledge. '
                                   'The response should be detailed, offering context and explanation to fully address the question. '
                                   'Use examples or suggestions where applicable, and consider specific dietary needs, cultural cuisines, '
                                   'or cooking techniques if mentioned in the question. '
                                   'Aim to make the information accessible and useful for informed kitchen practices or nutrition choices.\n')

                st.session_state["system_prompt"] = {"role": "system", "content": f"{task_definition}"}

            image_file = st.file_uploader("Upload an image of ingredients", type=["jpg", "png", "jpeg"])

            st.chat_input("Enter your message", on_submit=chat_actions, key="chat_input")

            for i in st.session_state["chat_history"]:
                with st.chat_message(name=i["role"]):
                    st.write(i["content"])

            if image_file is not None:
                temp_dir = 'temp'
                os.makedirs(temp_dir, exist_ok=True)

                image_path = os.path.join(temp_dir, image_file.name)
                with open(image_path, 'wb') as f:
                    f.write(image_file.read())

                ingredients = ["bacon", "cheese", "eggs", "tomatoes"]  # Placeholder!
                recipe = get_generated_recipe(ingredients)
                st.image(image_path)

                st.markdown("""
                                <style>
                                .big-font {
                                    font-size:60px !important;
                                }
                                </style>
                                """, unsafe_allow_html=True
                            )

                st.write("Recipe:")
                st.write(recipe)

