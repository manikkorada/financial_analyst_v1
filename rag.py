from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

GOOGLE_API_KEY = "AIzaSyCjEgh0zpshil21Cfragi0jMvfaNCnsZUU"


def get_pdf_text(pdf_file_path):
    text=""
    pdf_reader= PdfReader(pdf_file_path)
    for page in pdf_reader.pages:
        text+= page.extract_text()
    return  text


def get_text_chunks(raw_text):
    separators = [".", "!", "?"] + [" ", "\n", "\t"]
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        separators = separators,
        chunk_size=1024,
        chunk_overlap=100,
    )
    
    chunks = text_splitter.split_text(raw_text)
    return chunks

def get_vector_store(text_chunks, index_path):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001", google_api_key=GOOGLE_API_KEY)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local(index_path)


def chunk_and_index_documents(folder_path, index_path):

  
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)

            raw_text = get_pdf_text(file_path)
            text_chunks = get_text_chunks(raw_text)
            get_vector_store(text_chunks, index_path)

index_path = "faiss_index_rag"
docs_folder = "documents_rag"
if not os.path.exists(index_path):
    print("FAISS index not found. Creating new index...")
    chunk_and_index_documents("documents_rag", "faiss_index_rag")