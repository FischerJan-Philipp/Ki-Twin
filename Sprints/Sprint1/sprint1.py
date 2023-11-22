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

#os.environ["OPENAI_API_KEY"] = "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"

os.environ.get("OPENAI_API_KEY")

loader = PyPDFLoader('Logistik ZUSAMMENFASSUNG.pdf')
pages = loader.load_and_split()

text=[]
for page in pages:
    text.append(page.page_content)

combinedPDF = " ".join(text)




text_splitter = CharacterTextSplitter(
        #100 characters per chunk
        chunk_size=100, chunk_overlap=10
    )

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 100,
    chunk_overlap  = 20,
    length_function = len,
    add_start_index = True,
)

docs = text_splitter.create_documents([combinedPDF])
print(docs[2].page_content)

#create embeddings
faiss_index = FAISS.from_documents(docs, OpenAIEmbeddings())

#save the index database
faiss_index.save_local("faiss_logistikPDF_chunk_100_overlap_10")

#load the index database
db = FAISS.load_local("faiss_index", OpenAIEmbeddings())

#similarity search function
def retrieve_info(query):
    similar_documents = faiss_index.similarity_search(query, k=3)
    page_contents_array = [doc.page_content for doc in similar_documents]
    print(page_contents_array)
    return page_contents_array

#similarity search
query = "Was sind die Aufgaben der Logsitik?"
similar_documents = retrieve_info(query)
similar_documents[1].page_content


#2. Setup GPT and template
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")

template = """
    You are a student working with the following notes:
    {notes}
    1/ Your answers should be in the style of the notes you have read, only use the given information there.
    2/ If there is no relevant information in the notes, say "I don't know".
    
    Please write the best response that you can.
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["notes"]
)

chain = LLMChain(llm=llm, prompt=prompt)

#3.Retrieval augmented generation
def generate_response(query):
    notes = retrieve_info(query)
    response = chain.run(notes=notes)
    return response

response = generate_response(query)
print(response)