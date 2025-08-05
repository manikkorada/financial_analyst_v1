Financial Analyst Agent
This project is an AI-powered Financial Analyst Agent that helps users get real-time stock prices and insights from company reports (like annual filings). It uses tools such as Retrieval-Augmented Generation (RAG) and stock market APIs to answer user queries intelligently.

-> Features
Get NVDA Stock Prices
Retrieve current or historical stock prices of NVIDIA (NVDA) using the yfinance library.

-> Company Report Insights
Retrieve business, risk, or financial information from company documents (like 10-K reports) using RAG with FAISS vector DB.

-> Tool-based Decision Making
Dynamically invokes tools based on user query type:
get_nvda_stock_price: For stock price queries.
retrieval_rag_v1: For business/financial document insights.
Invokes both if required.

-> Tech Stack
LangGraph – For building agent workflow with nodes and edges.
FAISS Vector DB – For document retrieval.
LangChain – Tool integration and prompt chaining.
yfinance – Real-time & historical stock data.
LangChain Tools – Custom tools for query-specific execution.

-> Models Used here:
Embeddings - GoogleGnerative Embediigs Model(models/embedding-001)
LLM - llama3-70b

-> How It Works
1) User inputs a query, e.g.,
    “What is the current stock price of NVDA?”
    “What are the risks mentioned in NVIDIA’s 2024 annual report?”
    “Give me both stock price and key risks.”

2) The LLM with tool calling decides:

    Which tools to use (stock, retrieval, or both)
    Passes the state accordingly.

3) Responses from tools are combined and returned to the user.

Attcahed the screenshots of sample output and LangGrapg flow.