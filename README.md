# 496_CookBuddyProject

This project aims to create a cooking/nutrition helper app by leveraging LLMs and Object Detection models. 

The app currently provides the following features:

* User Authentication

User credentials and personal information are stored inside a Postgres database.
This database is later used to personalize the user's chat experience with the AI assistant.
Currently, the system stores the following fields as part of the user's profile:

1. Username
2. Password
3. First and Last Name
4. Age
5. Allergies
6. Dietary Restrictions

* Personalized Chat with an AI Assistant

The project provides a Chatbot interface for the user to chat with CookBuddy, an AI-based personal cooking/nutrition assistant. 

CookBuddy's LLM is TheBloke/Mistral-7B-instruct-v0.1.Q3.K_M, a quantized version of the preexisting Mistral-7B-instruct-v0.1 model.

This model provides capability for both creating unique recipes and answering general nutrition related questions. This is accomplished through a robust system prompt that also ensures the model refrains from providing harmful or unrelated information.

CookBuddy aims to provide personalized outputs, for which the user's name, allergies and dietary restrictions are provided as part of said system prompt.

* Object Detection-based Recipe Creation

Using a YOLOv8 model trained on a wide array of ingredients, the project can detect the contents of a user's refrigerator and leverage the LLM to provide a recipe using said contents.


* Helper Utilities

This project leverages the Spoonacular API to enhance the LLM's recipe outputs and provide certain utilities to make the user's cooking experience smoother.

Currently, the user can access the Spoonacular database for existing recipes that satisfy certain conditions, and can convert common cooking units of measurement to one another.

* Localized Hosting

The project eschews paid services such as OpenAI and Heroku in favor of free and locally runnable alternatives. This stance is based on privacy and budget concerns. In its current state, the project does not share sensitive with third parties, and can be deployed even from personal devices such as laptops. 

The Web UI was designed with Streamlit, and the LLM was deployed using LM Studio, an LLM hosting application based on the llama.cpp library.

Designing the UI with Streamlit allows this project to be accessed comfortably through both PCs and mobile devices.

The project is currently deployed through a Ngrok tunnel, so as not to rely on paid and external hosting services. The current URL of this project is as follows:

dog-finer-antelope.ngrok-free.app

