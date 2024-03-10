import yaml
import streamlit as st
import requests
import os
from pyngrok import ngrok

with open("config.yaml") as stream:
    try:
        config = yaml.safe_load(stream)
        inference_server_url = config["external_urls"]["inference"]
        recipe_server_url = config["external_urls"]["local_recipe"]
        ngrok_auth_token = config["auth_tokens"]["ngrok"]
        ngrok_url = config["external_urls"]["ngrok_url"]
    except yaml.YAMLError as exc:
        print(exc)

ngrok.set_auth_token(ngrok_auth_token)
http_tunnel = ngrok.connect(bind_tls=True, domain=ngrok_url, addr="8501")
print(http_tunnel)

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


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = {"role": "system", "content": f"{task_definition}"}

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
