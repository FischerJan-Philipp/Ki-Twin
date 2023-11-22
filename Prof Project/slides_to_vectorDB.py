import numpy as np
import faiss
import openai
import os
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

directory = './Sources/Data/Prof/Slides/'

# Initialize an empty list to store the contents of the text files
text_array = []

# Iterate over each file in the directory
for filename in os.listdir(directory):
    # Check if the file is a text file
    if filename.endswith('.txt'):
        # Open the text file
        with open(os.path.join(directory, filename), 'r') as f:
            # Read the contents of the text file
            text = f.read()
            # Add the contents to the list
            text_array.append(text)

one_string = ' '.join(text_array)


text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 1000,
    chunk_overlap  = 50,
    length_function = len,
    add_start_index = True,
)

docs = text_splitter.create_documents([one_string])

#create embeddings
faiss_index = FAISS.from_documents(docs, OpenAIEmbeddings())

#save the index database
faiss_index.save_local("Sources/Vector_DBs/prof_slides_1000_50_all_slides")

#load the index database
db = FAISS.load_local("Sources/Vector_DBs/prof_slides_1000_50_all_slides", OpenAIEmbeddings())
faiss_index = db