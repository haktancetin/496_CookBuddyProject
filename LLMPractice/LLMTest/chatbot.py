import os
import chainlit as cl
from langchain.chains import LLMChain
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
import getpass

key=load_dotenv()

model_id="flax-community/t5-recipe-generation"
conv_model=HuggingFaceHub(
                          repo_id=model_id,
                          model_kwargs={"temperature":0.8,"max_new_tokens":150})
template='''How to cook a meal using:
{query}
'''

@cl.on_chat_start
def main():
    prompt = PromptTemplate(template=template, input_variables=['query'])

    conv_chain = LLMChain(llm=conv_model, prompt=prompt, verbose=True)
    cl.user_session.set("llm_chain", conv_chain)

@cl.on_message
async def main(message:str):
    llm_chain=cl.user_session.get("llm_chain")
    res = await llm_chain.acall(message.content,callbacks=[cl.AsyncLangchainCallbackHandler()])
    await cl.Message(content=res["text"]).send()
