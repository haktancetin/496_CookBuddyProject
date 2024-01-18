import os
import chainlit as cl
from langchain import HuggingFaceHub, PromptTemplate,LLMChain
from getpass import getpass
HUGGINGFACEHUB_API_TOKEN = getpass()
os.environ['HUGGINGFACEHUB_API_TOKEN']=HUGGINGFACEHUB_API_TOKEN

model_id="gpt2-medium"
conv_model=HuggingFaceHub(huggingface_hub_api_token=os.environ['HUGGINGFACEHUB_API_TOKEN'],
                          repo_id=model_id,
                          model_kwargs={"temperature":0.8,"max_new_tokens":300})