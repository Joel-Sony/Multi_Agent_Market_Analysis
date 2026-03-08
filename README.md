# Collaborative Multi-Agent Market Analysis System (CrewAI + RAG)
This project analyzes customer reviews using AI.

The program reads a dataset of reviews, retrieves relevant feedback using a vector database, and then uses multiple AI agents to examine the data. Each agent performs a specific task such as identifying customer sentiment, finding common complaints, and detecting frequently praised features.

The system finally generates a structured report summarizing the overall sentiment, major issues mentioned by customers, positive aspects of the product or service, and business insights based on the reviews.      

- Sample_report: [View Report]('./market_analysis_report.md')

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