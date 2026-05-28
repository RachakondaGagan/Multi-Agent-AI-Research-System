from langchain.agents import create_agent
from langchain_openai import chatOpenAI
from langchain_core.prompt import ChatPromptTemplate
from langchain_core.output_parsers import StructuredOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv
import os
from rich import print

load_dotenv()

# Model setup
llm = chatOpenAI(model="gpt-4o-mini", temperature=0.0, api_key=os.getenv("OPENAI_API_KEY"))

# Agent 1
def build_search_agent():
    return create_agent(
        model = llm,
        tools = [web_search]
    )




