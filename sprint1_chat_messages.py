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

os.environ.get("OPENAI_API_KEY")

with open('gefilterte_nachrichten_emoji.txt') as f:
    chats = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 30,
    chunk_overlap  = 20,
    length_function = len,
    add_start_index = True,
)

docs = text_splitter.create_documents([chats])
print(docs[2].page_content)

#create embeddings
faiss_index = FAISS.from_documents(docs, OpenAIEmbeddings())

#save the index database
faiss_index.save_local("jan_chats_30_20")

#load the index database
db = FAISS.load_local("jan_chats_30_20", OpenAIEmbeddings())

#similarity search function
def retrieve_info(query):
    similar_documents = faiss_index.similarity_search(query, k=12)
    page_contents_array = [doc.page_content for doc in similar_documents]
    print(page_contents_array)
    return page_contents_array

#similarity search
query = "Wann gehen wir saufen bro?"
similar_documents = retrieve_info(query)
similar_documents[1].page_content


#2. Setup GPT and template
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")

template = """
    You are Jan, a business computing student at the HTW Berlin. You are chatting with your friend on WhatsApp.
    Your friends message is: {message}
    
    1/ Your answers should be in the style of your answers provided here: {chats}
    
    Please write the best response that you can.
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["message", "chats"]
)

chain = LLMChain(llm=llm, prompt=prompt)

#3.Retrieval augmented generation
def generate_response(query):
    chats = retrieve_info(query)
    response = chain.run(chats=chats, message=query)
    return response

response = generate_response(query)
print(response)