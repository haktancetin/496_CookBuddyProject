import json
import uuid
import streamlit as st
import requests
import os

inference_server_url = "http://placeholder.ngrok"
recipe_server_url = "http://127.0.0.1:5000"

def get_generated_recipe(ingredients:list):
    response = requests.get(url=recipe_server_url+"/generate_recipe", params={"ingredients": ingredients})
    return response.json()


st.set_page_config(
    page_title="CookBuddy App",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("CookBuddy ChatBot :female-cook:")
image_file = st.file_uploader("Upload an image of ingredients", type=["jpg", "png", "jpeg"])

with st.form('my_form'):
    text = st.text_area('Enter text:', 'Please enter a cooking/nutrition related query?')
    submitted = st.form_submit_button('Submit')
    # if not openai_api_key.startswith('sk-'):
    #     st.warning('Please enter your OpenAI API key!', icon='⚠')
    # if submitted and openai_api_key.startswith('sk-'):
    #     generate_response(text)

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
