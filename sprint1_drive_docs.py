from typing import List
import PyPDF2
import streamlit as st
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
import os
import getpass
from dotenv import load_dotenv

load_dotenv()

data_directory = "./Data"  # Path to your "Data" directory
text_contents = []  # Initialize an empty list to store the text content

for filename in os.listdir(data_directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(data_directory, filename)  # Full path to the file
        with open(file_path, "r", encoding="utf-8") as file:
            text_content = file.read()
            text_contents.append(text_content)

os.environ.get("OPENAI_API_KEY")
os.getenv("OPENAI_API_KEY")

with open('gefilterte_nachrichten_emoji.txt') as f:
    chats = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 200,
    chunk_overlap  = 20,
    length_function = len,
    add_start_index = True,
)

docs = text_splitter.create_documents([" ".join(text_contents)])
print(docs[2].page_content)

#create embeddings
faiss_index = FAISS.from_documents(docs, OpenAIEmbeddings())

#save the index database
faiss_index.save_local("kyrill_drive_docs_200_20")

#load the index database
db = FAISS.load_local("kyrill_drive_docs_100_20", OpenAIEmbeddings())
faiss_index = db
#similarity search function
def retrieve_info(query):
    similar_documents = faiss_index.similarity_search(query, k=30)
    page_contents_array = [doc.page_content for doc in similar_documents]
    print(page_contents_array)
    return page_contents_array

#similarity search
query = "Was studierst du und wie lange noch?"

#2. Setup GPT and template
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")

template = """
    You are Kyrill.
    You have this this information from you google drive:
    {information}
    
    1/ Your answers are on the knowledge base of that information
    2/ Answer all the questions in the best way and also in the style of the information you have read.
    3/ Always answer in the language of the question.
    
    Please write the best response that you can.
    
    The question/task is {query}
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["information", "query"]
)

chain = LLMChain(llm=llm, prompt=prompt)

#3.Retrieval augmented generation
def generate_response(query):
    information = retrieve_info(query)
    response = chain.run(information=information, query=query)
    return response
information = retrieve_info(query)

response = generate_response(query)
print(response)