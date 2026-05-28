# 🔬 ResearchMind

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.57-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.2-1C3C3A?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com)
[![Mistral AI](https://img.shields.io/badge/Mistral%20AI-Large-FF5E00?style=for-the-badge&logo=mistralai&logoColor=white)](https://mistral.ai)
[![Tavily](https://img.shields.io/badge/Tavily-Search%20API-FF8C00?style=for-the-badge&logo=googlechrome&logoColor=white)](https://tavily.com)

**An advanced, multi-agent AI research briefing dashboard that collaborates sequentially to generate professional, peer-reviewed intelligence briefings on any topic.**

[Explore Features](#-key-features) • [Orchestration Flow](#-agentic-orchestration-flow) • [Quick Start](#-quick-start) • [Deployment](#-cloud-deployment)

</div>

---

## 📌 Project Preview

<div align="center">
  <!-- Place your stunning SaaS dashboard screenshot here -->
  <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80" alt="ResearchMind Dashboard Preview" width="850" style="border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 20px 40px rgba(0,0,0,0.3);"/>
  <p><em>Premium obsidian-themed SaaS Workspace displaying real-time dynamic agent executions.</em></p>
</div>

---

## ⚡ Key Features

- **Collaborative Agent Network**: Orchestrates four specialized AI agents to crawl, extract, write, and validate research data.
- **Dynamic Real-Time Pipeline**: Dynamic, sequential UI state updates using Streamlit session state and stage transitions (`WAITING` ➔ `ACTIVE` ➔ `COMPLETE`).
- **Resilient Rate-Limiting**: Built-in cooling buffers (`time.sleep`) to seamlessly execute complex pipelines even on free-tier API accounts without triggering HTTP 429 errors.
- **Supportive Editorial Peer-Review**: Automatic constructive critique of your reports with generous grading scores and encouraging verdicts.
- **Instant Markdown Downloads**: Save and download beautifully generated intelligence briefs directly from your dashboard in standard Markdown format.

---

## 🛠️ Tech Stack

- **Frontend & Interface**: [Streamlit](https://streamlit.io) (Custom HSL Dark Mode CSS + Glassmorphism UI Layouts)
- **Agent Orchestration**: [LangChain Ecosystem](https://github.com/langchain-ai/langchain)
- **Large Language Model**: [Mistral AI](https://mistral.ai) (`ChatMistralAI` Native Integration)
- **Web Crawling**: [Tavily API](https://tavily.com) (Structured Search Engine) & BeautifulSoup4 (Custom Document Parser)

---

## 🔬 Agentic Orchestration Flow

```mermaid
graph TD
    User([User Input: Subject]) --> UI[Streamlit SaaS Workspace]
    UI -->|01. Trigger Pipeline| Agent1[Web Search Agent]
    Agent1 -->|Live Tavily Search| Tavily[Tavily Search API]
    Tavily -->|Aggregated Snippets & URLs| Agent2[Deep Document Scraper]
    Agent2 -->|Parse Webpages| BeautifulSoup[BeautifulSoup4 Scraper]
    BeautifulSoup -->|Clean Document Feed| Agent3[Principal Research Writer]
    Agent3 -->|Draft Executive Briefing| Agent4[Editorial Peer Critic]
    Agent4 -->|Constructive Peer Review| UI
    UI -->|Render Workspace| Download([Download Briefing .md])

    classDef default fill:#111827,stroke:#374151,stroke-width:1px,color:#E5E7EB;
    classDef agent fill:#1E1B4B,stroke:#6366F1,stroke-width:2px,color:#F8FAFC;
    classDef external fill:#271A0C,stroke:#F59E0B,stroke-width:1px,color:#FEF3C7;
    classDef final fill:#062F1F,stroke:#10B981,stroke-width:2px,color:#ECFDF5;

    class Agent1,Agent2,Agent3 agent;
    class Tavily,BeautifulSoup external;
    class Agent4,Download final;
```

---

## 👥 Meet Your AI Research Team

| Agent | Technology | Core Functionality |
| :--- | :--- | :--- |
| **01. Web Search Agent** | `TavilyClient` | Scans live search indexes and groups primary resources. |
| **02. Deep Document Scraper** | BeautifulSoup4 | Decomposes stylesheets and cleans navigation structures for deep content. |
| **03. Principal Research Writer** | LangChain LLM | Synthesizes raw text feeds and drafts professional intelligence briefs. |
| **04. Editorial Peer Critic** | LangChain LLM | Performs structured quality checks, issues score cards, and suggests enhancements. |

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/RachakondaGagan/Multi-Agent-AI-Research-System.git
cd Multi-Agent-AI-Research-System
```

### 2. Configure Environment Secrets
Create a `.env` file in the root directory:
```env
TAVILY_API_KEY = "your-tavily-api-key"
MISTRAL_API_KEY = "your-mistral-api-key"
```

### 3. Install Dependencies & Run
Setup your virtual environment and launch the dashboard:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## ☁️ Cloud Deployment

You can deploy this dashboard to the cloud completely for free in under 2 minutes using **Streamlit Community Cloud**:

1. Log in to [share.streamlit.io](https://share.streamlit.io/).
2. Click **New app** and connect your repository: `RachakondaGagan/Multi-Agent-AI-Research-System`.
3. In **Advanced Settings ➔ Secrets**, paste your API environment variables:
   ```toml
   TAVILY_API_KEY = "your-tavily-api-key"
   MISTRAL_API_KEY = "your-mistral-api-key"
   ```
4. Click **Deploy!**

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
