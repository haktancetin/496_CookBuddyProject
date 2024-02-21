# 496_CookBuddyProject - 

The project is currently composed of the following modules:

LLMRemoteConnection -> Google Colab Notebook (Used to host a pretrained Chat LLM with TGI for faster querying, accessed through ngrok)

recipe_generator_app.py -> Flask App (Used as an endpoint for querying the flax-community/t5-recipe-generation LLM)

app.py -> Streamlit ChatBot App (Main app, used by the customer to interface with the above two modules)

