from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_community.llms import HuggingFaceHub

from langchain.prompts import PromptTemplate

load_dotenv()

hub_llm=HuggingFaceHub(
    repo_id="flax-community/t5-recipe-generation",
    model_kwargs={'temperature':0.7,'max_length':300}
)

print("Start chat")
request= input()
prompt=PromptTemplate(
    input_variables=["Ingredients"],
    template=request+" {Ingredients}"
)
hub_chain=LLMChain(prompt=prompt,llm=hub_llm,verbose=True)
print(hub_chain.run("meat,potato,tomato and garlic"))