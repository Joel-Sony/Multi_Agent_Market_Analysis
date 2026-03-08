# Collaborative Multi-Agent Market Analysis System (CrewAI + RAG)

This project implements a Collaborative Multi-Agent Market Analysis System using CrewAI and Retrieval-Augmented Generation (RAG).

The system analyzes customer reviews and generates structured business insights.
Multiple AI agents with specialized roles work together to extract sentiment, identify patterns in customer feedback, and produce a final market analysis report.

The goal is to demonstrate how multi-agent AI systems can automate market intelligence from large collections of textual data.

--- 
## Features

- Retrieval-Augmented Generation (RAG) for contextual analysis
- Multi-agent collaboration using CrewAI
- Real customer review dataset
- Structured Markdown report generation
- Market insights and business recommendations

___ 
## Project Structure
```  
Multi_Agent_Market_Analysis/    
│  
├── main.py  
├── reviews.csv  
├── market_analysis_report.md  
└── README.md  
```

- ###  main.py  
Main pipeline implementing RAG retrieval and CrewAI agent collaboration.  
 
- ### reviews.csv  
Dataset containing customer review text used for analysis.  

- ### market_analysis_report.md  
Generated market analysis report.  

---
## Installation
 
Clone the repository and install dependencies.
```
pip install crewai crewai-tools litellm  
pip install langchain langchain-community langchain-huggingface  
pip install chromadb sentence-transformers pandas  
```
### API Key Setup  

This project uses Groq LLM (Llama-3).  

Set your API key as an environment variable:  
```
export GROQ_API_KEY="your_api_key_here"  
```

### Running the System  

Execute the pipeline:  
```
python3 main.py  
```

The system will:   
- Load the review dataset  
- Convert reviews into embeddings  
- Store them in a vector database  
- Retrieve relevant reviews using RAG  
- Run multiple AI agents for analysis  
- Generate a structured market report   


### Technologies Used  

- CrewAI (Multi-Agent AI Framework)  
- LangChain  
- Chroma Vector Database 
- Sentence Transformers   
- Groq Llama-3 LLM  

---
## Conclusion  

This system demonstrates how multi-agent AI architectures combined with retrieval-based knowledge systems can automate large-scale analysis of customer feedback and generate actionable business insights.  