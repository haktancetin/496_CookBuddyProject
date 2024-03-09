# 496_CookBuddyProject - 

The project is currently composed of the following modules:

1. recipe_generator_app.py -> Flask App (Used as an endpoint for querying the flax-community/t5-recipe-generation LLM)

2. app.py -> Streamlit ChatBot App (Main app, used by the customer to interface with the above two modules)

For the Streamlit ChatBot to work, config.yaml must be created and filled in as outlined in config_template.yaml.

Currently, this LLM module connects to an inference server set up by LM Studio. 
This server's optimization features allow for an LLM to be run on a standard personal computer without performance issues.

