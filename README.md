# 496_CookBuddyProject

This project aims to create a cooking/nutrition helper app by leveraging LLMs and Object Detection models. 

## User Authentication

User credentials and personal information are stored inside a Postgres database.
This database is later used to personalize the user's chat experience with the AI assistant.
Currently, the system stores the following fields as part of the user's profile:

1. Username
2. Password
3. First and Last Name
4. Age
5. Allergies
6. Dietary Restrictions

## Personalized Chat with an AI Assistant

The project provides a Chatbot interface for the user to chat with CookBuddy, an AI-based personal cooking/nutrition assistant. 

CookBuddy's LLM is TheBloke/Mistral-7B-instruct-v0.1.Q3.K_M, a quantized version of the preexisting Mistral-7B-instruct-v0.1 model.

This model provides capability for both creating unique recipes and answering general nutrition related questions. This is accomplished through a robust system prompt that also ensures the model refrains from providing harmful or unrelated information.

CookBuddy aims to provide personalized outputs, for which the user's name, allergies and dietary restrictions are provided as part of said system prompt.

## Object Detection-based Recipe Creation

Using a YOLOv8 model trained on a wide array of ingredients, the project can detect the contents of a user's refrigerator and leverage the LLM to provide a recipe using said contents.


## Helper Utilities

This project leverages the Spoonacular API to enhance the LLM's recipe outputs and provide certain utilities to make the user's cooking experience smoother.

Currently, the user can access the Spoonacular database for existing recipes that satisfy certain conditions, and can convert common cooking units of measurement to one another. It is also possible to augment AI-generated recipes by estimating calories based off of the recipe's title.

## Localized and High Performance Hosting

The project eschews paid services such as OpenAI and Heroku in favor of free and locally runnable alternatives. This stance is based on privacy and budget concerns. In its current state, the project does not share sensitive data with third parties, and can be deployed even from personal devices such as laptops. 

## Used Frameworks and Technologies

The Web UI was designed with Streamlit, and the LLM was deployed using LM Studio, an LLM hosting application based on the llama.cpp library.

Designing the UI with Streamlit allows this project to be accessed comfortably through both PCs and mobile devices.

The project is currently deployed through a Ngrok tunnel, so as not to rely on paid and external hosting services. The current URL of this project is as follows:

dog-finer-antelope.ngrok-free.app

## Project Setup

To run the project on a local machine, the following steps have to be taken:

1. An inference server must be set up, preferably through llama.cpp or LM Studio.
2. The config.yaml file must be created based on config_template.yaml.
2. The URL of the inference server must be added to config.yaml.
3. A Spoonacular API token must be added to config.yaml.
4. The secrets.toml file must be updated with the relevant database information.
4. The project's required packages must be installed, preferably by running the command ```pip install -r requirements.txt```.
5. The command ```streamlit run main.py``` must be entered.
6. Deploying the project is left to the user's discretion. Currently, deployment is handled through a Ngrok tunnel.

