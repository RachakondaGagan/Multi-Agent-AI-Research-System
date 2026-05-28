from langchain.agents import create_agent
from langchain_openai import chatOpenAI
from langchain_core.prompts import ChatPromptTemplate
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

# Agent 2
def build_scrape_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url]
    )

# Writer Chain
write_prompt = chatPromptTemplate.from_messages([
    ('system', 'You are an expert research writer. Write clear, structured and insightful reports.'),
    ('human', """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])
writer_chain = write_prompt | llm | StrOutputParser()

