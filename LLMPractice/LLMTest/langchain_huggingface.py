from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_community.llms import HuggingFaceHub

from langchain.prompts import PromptTemplate

load_dotenv()
hub_llm=HuggingFaceHub(repo_id="mrm8488/t5-base-finetuned-wikiSQL")
prompt=PromptTemplate(
    input_variables=["question"],
    template="Translate English to SQL: {question}"
)
hub_chain=LLMChain(prompt=prompt,llm=hub_llm,verbose=True)
print(hub_chain.run("what ist the average of the respondents using a mobile device?"))

hub_llm=HuggingFaceHub(
    repo_id="flax-community/t5-recipe-generation",
    model_kwargs={'temperature':0.7,'max_length':300}
)
prompt=PromptTemplate(
    input_variables=["Ingredients"],
    template="Tell me a recipe which include: {Ingredients}"
)
hub_chain=LLMChain(prompt=prompt,llm=hub_llm,verbose=True)
print(hub_chain.run("meat, potato and tomato"))

prompt=PromptTemplate(
    input_variables=["Ingredients"],
    template="How to cook a meal with using: {Ingredients}"
)
hub_chain=LLMChain(prompt=prompt,llm=hub_llm,verbose=True)
print(hub_chain.run("meat, potato and tomato"))

print("Start chat")
request= input()
prompt=PromptTemplate(
    input_variables=["Ingredients"],
    template=request+" {Ingredients}"
)
hub_chain=LLMChain(prompt=prompt,llm=hub_llm,verbose=True)
print(hub_chain.run("meat,potato,tomato and garlic"))