<div align="center">

# 🤖 Multi-Agent Market Analysis System

### CrewAI + RAG-Powered Collaborative Intelligence

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-6366F1?style=for-the-badge)](https://crewai.com)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C?style=for-the-badge)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-F55036?style=for-the-badge)](https://groq.com)
[![Flask](https://img.shields.io/badge/Flask-Web_App-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

*A team of 4 specialized AI agents collaboratively analyze unstructured product reviews using Retrieval-Augmented Generation to produce executive-ready market insights via a premium web dashboard.*

<img src="./dashboard_preview.png" alt="Dashboard Preview" width="800"/>

---

</div>

## Key Features


###  Advanced AI Architecture
- **Retrieval-Augmented Generation (RAG):** Processes datasets too large for standard LLM context windows. Uses `ChromaDB` and HuggingFace `all-MiniLM-L6-v2` embeddings to pinpoint and retrieve only the statistically relevant reviews based on your specific analytical query.
- **Multi-Agent Collaboration:** Employs **CrewAI** to orchestrate four distinct personas, simulating a real-world analytics department. Each agent builds upon the previous agent's findings, producing deep, nuanced synthesis rather than shallow summaries.
- **Llama 3.3 70B Integration:** Powered by Groq's blazing-fast inference API, leveraging a massive 70-billion parameter model for unparalleled cognitive reasoning.

### Premium Web Dashboard (Flask + Vanilla JavaScript)
- **Glassmorphism Dark Theme UI:** A sleek, modern user interface built from scratch without bloated CSS frameworks. Features subtle ambient background glows, micro-interactions, and responsive layout grids.
- **Live Dataset Statistics:** Animated counter cards dynamically read the underlying CSV to display total reviews, exact positive/negative splits, and character distributions.
- **Interactive Sentiment Charting:** Real-time data visualization via `Chart.js`, rendered as an animated, tooltip-enabled doughnut chart.
- **Real-Time Analysis Polling:** The "Run Analysis" interface transforms into a live status tracker, showing exactly which AI agent is currently "thinking" and what sub-task they are executing.
- **In-Browser Markdown Rendering:** Final strategic reports are compiled, styled, and rendered directly in the dashboard UI using `marked.js`, fully formatted with tables, lists, and headers.
- **Report History Management:** A persistent sidebar automatically tracks, saves, and lists all prior analysis runs, allowing one-click reloading of historical market research.

###  Production-Ready Modularity
- **Modular Codebase:** Completely refactored from a monolithic script into specialized Python modules (`rag/`, `agents/`, `tasks/`, `config.py`), adhering to software engineering best practices.
- **Robust Orchestration Engine:** The `crew.py` core cleanly injects dependencies and manages the asynchronous hand-offs between the embedding vector store and the LLM workers.

---

## System Architecture
### The 4 Specialized Agent Roles

1. **Sentiment Analyst:** Classifies overall sentiment, identifying core emotional patterns and estimating positive/negative feature satisfaction ratios.
2.  **Trend Analyst:** Extracts recurring complaints, most praised features, and emerging shifts in customer expectations.
3.  **Competitor Analyst:** Scans for indirect competitor mentions, assessing market positioning and competitive gaps.
4.  **Business Strategist:** Synthesizes the previous three agents' findings into a final, highly structured, executive-ready report with prioritized recommendations.

---

##  Quick Start

### 1. Clone & Install Environment

```bash
# Clone repository
git clone https://github.com/your-username/Multi_Agent_Market_Analysis.git
cd Multi_Agent_Market_Analysis

# Create isolated virtual environment
python3 -m venv venv
source venv/bin/activate

# Install lean, project-specific dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root containing your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Launch the Server

Run the Flask application:
```bash
python3 app.py
```

Open your browser and navigate to: **`http://localhost:5000`**

---

## Usage Options

### Active Dashboard Analysis
1. View the **Dataset Overview** and **Sentiment Distribution** on load.
2. In the **Run Analysis** card, enter a specific focal query (e.g., *"What do customers say about battery life and delivery speed?"*).
3. Click **Start Analysis**. The UI will display live updates as the RAG pipeline builds embeddings and the 4 agents perform their work.
4. Review the generated Markdown report instantly in the browser or download it.

### Command Line Interface
If you prefer running analyses headlessly:
```bash
python3 run_analysis.py --query "overall durability and customer support complaints"
```
The final report will be dumped to stdout and saved sequentially in the `/output` folder.

---

## 📄 Output Data Sample

Reports include detailed sections such as:
- Executive Summary
- Sentiment Analysis Breakdown
- Ranked Customer Complaints & Pain Points
- Praised Features & Product Strengths
- Market Trends & Patterns
- Competitive Landscape Assessment
- Strategic Actionable Recommendations

---

## 📝 License

This project is licensed under the Apache License 2.0 — see the [LICENSE](./LICENSE) file for details.