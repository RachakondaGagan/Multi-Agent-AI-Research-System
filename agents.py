from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

from tools import web_search, scrape_url
from dotenv import load_dotenv
import os
from rich import print

load_dotenv()

# Model setup
# Official Mistral AI model integration
llm = ChatMistralAI(
    model=os.getenv("MISTRAL_MODEL", "mistral-large-latest"),
    temperature=0.0,
    api_key=os.getenv("MISTRAL_API_KEY") or os.getenv("MISTRAL_APIKEY"),
)

# Agent 1
def build_search_agent():
    return create_agent(
        model = llm,
        tools = [web_search]
    )

# Agent 2 (Reader/Scraper)
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
    )


# Writer Chain
write_prompt = ChatPromptTemplate.from_messages([
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
from langchain_core.output_parsers import StrOutputParser
writer_chain = write_prompt | llm | StrOutputParser()

# Critic Chain 
critic_prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are a critical analyst. Evaluate the quality of research and writing.'),
    ('human', """Evaluate the following research report based on:
    - Depth of research (Did it cover key aspects of the topic?)
    - Clarity and structure of writing
    - Use of sources (Were the sources relevant and well-integrated?)

    Report:
    {report}
     
     Respond in this format:

    Score: X/10

    Strengths:
    - ...
    - ...

    Areas to Improve:
    - ...
    - ...

    One line verdict:

Provide a detailed critique with suggestions for improvement."""),
])
critic_chain = critic_prompt | llm | StrOutputParser()


