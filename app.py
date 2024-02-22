import json
import uuid
import yaml
import streamlit as st
import requests
import string
import random
import os

with open("config.yaml") as stream:
    try:
        config = yaml.safe_load(stream)
        inference_server_url = config["external_urls"]["inference"]
        recipe_server_url = config["external_urls"]["local_recipe"]
    except yaml.YAMLError as exc:
        print(exc)


def random_string():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


def chat_actions():
    st.session_state["chat_history"].append(
        {"role": "user", "content": st.session_state["chat_input"]},
    )

    query = st.session_state["chat_input"]
    response = get_query_response(string=query)

    st.session_state["chat_history"].append(
        {
            "role": "assistant",
            "content": response,
        },
    )


def get_generated_recipe(ingredients: list):
    response = requests.get(url=recipe_server_url + "/generate_recipe", params={"ingredients": ingredients})
    return response.json()


def get_query_response(prompt: str):
    params_dic = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 512}
    }
    response = requests.post(url=inference_server_url + "/generate", params=params_dic)
    return response.json()


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.set_page_config(
    page_title="CookBuddy App",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("CookBuddy ChatBot :female-cook:")
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
    # st.write(f'<p class="big-font">' + full_recipe + '</p>', unsafe_allow_html=True, fontsize=100)
