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
    ('system', 'You are a world-class principal research analyst and writer. Your reports are authoritative, professional, and visually stunning, utilising clean Markdown headers, bullet points, and highlighted sections.'),
    ('human', """Produce a comprehensive, highly-detailed, and authoritative research report on the following topic.
    
Topic: {topic}

Research Data Gathered:
{research}

Format your report perfectly with the following structure:
# {topic}
*An in-depth intelligence briefing on {topic}.*

---

## 1. Executive Summary
Provide a high-level, elegant summary of the current landscape, key trends, and core insights.

## 2. In-Depth Analysis & Key Findings
Elaborate on at least 3 major findings. Under each finding, include:
- A bold, descriptive sub-heading.
- A detailed explanation of the technological/scientific mechanism or real-world application.
- A summary of current challenges or future outlook.

## 3. Key Takeaways & Actionable Insights
Provide a concise bulleted list of the most critical learnings from this research.

## 4. References & Sources
List all URLs and sources found in the research cleanly as markdown links or citations.

Ensure the tone is analytical, sophisticated, and highly informative. Do not use placeholders."""),
])
from langchain_core.output_parsers import StrOutputParser
writer_chain = write_prompt | llm | StrOutputParser()

# Critic Chain 
critic_prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are a supportive editorial director. Your role is to provide a constructive, encouraging, and balanced peer-review. Focus on highlighting strengths and give fair, highly positive scores for well-structured research. Keep suggestions concise and polite.'),
    ('human', """Review the following research report and provide a constructive editorial evaluation. Since the writer is a top-tier analyst, maintain a positive, encouraging tone. Ensure your score is generous (e.g. 8/10 to 10/10) if the report is detailed and accurate.

Report to Review:
{report}

Please respond strictly using the following clean, concise format:

### 📋 Peer Review Summary

- **Overall Quality Score**: **X/10** *(Award high scores for comprehensive research)*
- **Key Strengths**:
  - [Highlight a major strength]
  - [Highlight a second strength]
- **Constructive Enhancements**:
  - [Suggest 1 optional minor enhancement]
- **Editorial Verdict**: *[A single line of positive, professional encouragement]*
"""),
])
critic_chain = critic_prompt | llm | StrOutputParser()
