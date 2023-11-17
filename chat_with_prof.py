import pandas as pd
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
import openai
from datetime import datetime
import json
import os


load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]



class ProfChat:
    def __init__(self):

        self.db = FAISS.load_local("./Vector_DBs/prof_transcript_300_30", OpenAIEmbeddings())

    def retrieve_info(self, query):
        similar_documents = self.db.similarity_search(query, k=3)
        page_contents_array = [doc.page_content for doc in similar_documents]
        print(page_contents_array)
        return page_contents_array

    def get_answer(self, query):
        f = open('./Prompt_Templates/chat_calendar.txt', "r")
        prompt = f.read()
        prompt = prompt.replace("<query>", query)
        prompt = prompt.replace("<style>", " ".join(self.retrieve_info(query)))
        prompt = prompt.replace("<slides>", str(datetime.now()))
        prompt = prompt.replace("<date>", str(datetime.now()))

        print("PROMPT LENGTH: " + str(len(prompt)))
        print(prompt)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content

    def test(self, query):
        prompt_template = open('./Prompt_Templates/prof_prompt.txt', "r")
        prompt = prompt_template.read()
        prompt = prompt.replace("<query>", query)
        prompt = prompt.replace("<style>", " ".join(self.retrieve_info(query)))
        prompt = prompt.replace("<slides>", str(datetime.now()))
        prompt = prompt.replace("<date>", str(datetime.now()))

        print("PROMPT LENGTH: " + str(len(prompt)))
        print(prompt)


        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content


#chat = ChatCalendar()

#query = "Hast du Lust dich die Tage zu treffen?"
#response = chat.test(query=query)

#print(response)


