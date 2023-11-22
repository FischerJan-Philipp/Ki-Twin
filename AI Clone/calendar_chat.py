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



class ChatCalendar:
    def __init__(self):
        self.calendar_data = pd.read_csv('../Sources/Data/Calendar/768873652410-fjtsnuivvv6c6gukbqq0gga1jvaiklp3.apps.googleusercontent.com.csv')

        chat_messages = []

        with open('../Sources/Data/Chat/gefilterte_nachrichten_emoji.txt', 'r', encoding='utf-8') as chat_data_file:
            for line in chat_data_file:
                chat_messages.append(line.strip())

        self.chat_data = pd.DataFrame({'ChatMessages': chat_messages})

        self.db = FAISS.load_local("../Sources/Vector_DBs/jan_chats_100_20", OpenAIEmbeddings())

    def retrieve_info(self, query):
        similar_documents = self.db.similarity_search(query, k=10)
        page_contents_array = [doc.page_content for doc in similar_documents]
        print(page_contents_array)
        return page_contents_array

    def get_relevant_calendar_event(self, query):

        prompt = f"The query is: {query}, today is: {datetime.now().strftime('%Y-%m-%d %H:%M:%S%z')}"
        cd = pd.read_csv('../Sources/Data/Calendar/768873652410-fjtsnuivvv6c6gukbqq0gga1jvaiklp3.apps.googleusercontent.com.csv')

        relevant_data_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[{"role": "user", "content": prompt}],
            functions=[
                {
                    "name": "get_relevant_timeframe",
                    "description": "Get the relevant timeframe to look at in the calendar data for a certain query. The date format is: '2013-02-14T13:15:03-08:00' (YYYY-MM-DDTHH:mm:ssZ) ",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "start": {
                                "type": "string",
                                "description": "start date of the timeframe",
                            },
                            "end": {
                                "type": "string",
                                "description": "end date of the timeframe"
                            },
                        },
                        "required": ["start", "end"],
                    },
                }
            ],
            function_call={"name": "get_relevant_timeframe"},
        )

        json_response = json.loads(relevant_data_response['choices'][0]['message']['function_call']['arguments'])
        print(json_response)
        # Convert the "start" and "end" strings from the JSON response to datetime objects
        start = datetime.strptime(json_response['start'], '%Y-%m-%dT%H:%M:%S%z')
        end = datetime.strptime(json_response['end'], '%Y-%m-%dT%H:%M:%S%z')
        print(start)
        print(end)
        # Ensure that the "start" column is in datetime format
        cd = cd[~cd['start'].str.match(r'\d{4}-\d{2}-\d{2}$')]

        cd['start'] = pd.to_datetime(cd['start'])

        # Perform the date comparison
        filtered_df = cd[(cd['start'] >= start) & (cd['start'] <= end)]

        return filtered_df


    def get_answer(self, query):
        f = open('../Sources/Prompt_Templates/chat_calendar.txt', "r")
        prompt = f.read()
        prompt = prompt.replace("<query>", query)
        prompt = prompt.replace("<Calendar_Data>", self.get_relevant_calendar_event(query).to_string())
        prompt = prompt.replace("<Chat_Data>", " ".join(self.retrieve_info(query)))
        prompt = prompt.replace("<date>", str(datetime.now()))

        print("PROMPT LENGTH: " + str(len(prompt)))
        print(prompt)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content

    def test(self, query):
        prompt_template = open('../Sources/Prompt_Templates/chat_calendar.txt', "r")
        prompt = prompt_template.read()
        prompt = prompt.replace("<query>", query)
        prompt = prompt.replace("<Calendar_Data>", self.get_relevant_calendar_event(query).to_string())
        prompt = prompt.replace("<Chat_Data>", " ".join(self.retrieve_info(query)))
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


