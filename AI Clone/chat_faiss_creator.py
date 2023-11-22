from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

chat_messages = []

with open('../Sources/Data/Chat/gefilterte_nachrichten_emoji.txt', 'r', encoding='utf-8') as chat_data_file:
    for line in chat_data_file:
        chat_messages.append(line.strip())

chat_data = pd.DataFrame({'ChatMessages': chat_messages})

chat_data.to_csv(f'./Data/Chat/jan_chats.csv', index=False)

loader = CSVLoader(f'../Sources/Data/Chat/jan_chats.csv')
index_creator = VectorstoreIndexCreator()
index = index_creator.from_loaders([loader])
chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=index.vectorstore.as_retriever(), input_key="question")
