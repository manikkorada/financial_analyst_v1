from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS

from langchain_core.documents import Document
from langgraph.graph import START, StateGraph, END
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

from langgraph.graph.message import add_messages
import yfinance as yf
from typing import Annotated
from typing_extensions import TypedDict, List
import ast


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages:Annotated[list,add_messages]
   
llm=init_chat_model("groq:llama3-70b-8192", api_key = GROQ_API_KEY)

embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001", google_api_key=GOOGLE_API_KEY)
new_db = FAISS.load_local("faiss_index_rag", embeddings, allow_dangerous_deserialization=True)
retriever = new_db.as_retriever(search_kwargs={"k": 4})


def retrieval_rag_v1(query:str):
    """Utilize this tool If user asks about the company information other than stock price values using the query
    
    Args:
        query (str) 

    Based on the query below function retrieve the similar documents.

    Returns:
        str: output str
    """
    retrieve_text = ""
    docs = retriever.invoke(query)
    for i in docs:
        retrieve_text += i.page_content

    return retrieve_text

def get_nvda_stock_price(date_str : str):
    """Utilize this tool only to get the stock market price of current date or if user mentioned any date please extract of that particular date

    Args : 
        date : Str of Date YYYY-MM-DD or empty str

    Returns:
        str: output str
    
    """
    
    try:
        if date_str == " ":
            current_price = ticker.history(period="1d")["Close"].iloc[-1]
            return f"The current stock price is${current_price:.2f}"
            
        ticker = yf.Ticker("NVDA")
        price = ticker.history(start=date_str, period="1d")["Close"].iloc[-1]
        if price:
            return f"NVDA stock price on {date_str} was ${price:.2f}"

    except Exception as e:
        return f"An error occurred while fetching the stock price: {str(e)} or No data available for {date_str} — it may be a holiday or weekend."

prompt_financial_analyst = '''
        You are a financial analyst agent specialized in retrieving financial data.
        
        You have access to the following tools:
        `get_nvda_stock_price`: Use this tool to get current or historical NVDA stock prices.
        `retrieval_rag_v1`: Use this tool to get annual report insights from a NVDIA company.

        ##get_nvda_stock_price Instructions:
        - Input to this tool is date. You must pass the date to this tool as a arguement.
        - If the user mentions only a **month and year**, assume the **1st day** of that month.
        - If the user asks for the **current stock price**, pass empty string as a arguement.

        ## retrieval_rag_v1 Instructions:
        - Goal is to generate an ANSWER for the QUESTION, based on the provided SOURCES.
        - You will be given a list of SOURCES that you can use to ANSWER the QUESTION. 
        - You must use the SOURCES to ANSWER the QUESTION. 
        - You must not use any other SOURCES. 
        
        You must:
        Use `get_nvda_stock_price` only if the user asks about the current stock price or price on a specific date.
        Use `retrieval_rag_v1` for any company-related questions such as risks, business operations, or financial statements.
        Use **both tools** if the query includes both aspects.
        Always return a helpful answer in simple terms.
    '''



tools = [get_nvda_stock_price, retrieval_rag_v1]
llm_with_tool=llm.bind_tools(tools)

## Node definition
def financial_analyst(state:State):
    messages = [SystemMessage(content=prompt_financial_analyst),] + state['messages']
    return {"messages":[llm_with_tool.invoke(messages)]}

## Grpah
builder=StateGraph(State)
builder.add_node("financial_analyst",financial_analyst)
builder.add_node("tools",ToolNode(tools))

## Add Edges
builder.add_edge(START, "financial_analyst")
builder.add_conditional_edges("financial_analyst",tools_condition)
builder.add_edge("tools","financial_analyst")

## compile the graph
graph=builder.compile()

user_input = input()
response=graph.invoke({"messages":user_input})
for m in response['messages']:
    m.pretty_print()