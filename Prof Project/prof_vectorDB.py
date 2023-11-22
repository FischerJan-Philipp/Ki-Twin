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

with open('../Sources/Data/Prof/transcript.txt') as f:
    transcript = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=300,
    chunk_overlap=30,
    length_function=len,
    add_start_index=True,
)

docs = text_splitter.create_documents([transcript])
print(docs[2].page_content)

# create embeddings
faiss_index = FAISS.from_documents(docs, OpenAIEmbeddings())

# save the index database
faiss_index.save_local("./Sources/Vector_DBs/prof_transcript_300_30")

# load the index database
db = FAISS.load_local("./Sources/Vector_DBs/prof_transcript_300_30", OpenAIEmbeddings())
faiss_index = db


# similarity search function
def retrieve_info(query):
    similar_documents = faiss_index.similarity_search(query, k=3)
    page_contents_array = [doc.page_content for doc in similar_documents]
    print(page_contents_array)
    return page_contents_array


# similarity search
query = "Was ist ein neuronales netzwerk genau?"

# 2. Setup GPT and template
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")

template = """
    You are Axel Hochstein, a Business Computing professor at the HTW Berlin. You answer to any kinds of questions and tasks about your lectures in the module "Application of Artificial Intelligence".
    You got the message: {message}

    1. Your answers should be in the style of your previouse lectures, parts of those are provided here: {info}
    2. Always answer in a way that is matches your lecture style.

    Please write the best response that you can.
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["message", "chats"]
)

chain = LLMChain(llm=llm, prompt=prompt)


# 3.Retrieval augmented generation
def generate_response(query):
    info = retrieve_info(query)
    response = chain.run(chats=info, message=query)
    return response


response = generate_response(query)
print(response)