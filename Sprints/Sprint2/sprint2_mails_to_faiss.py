from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from Sources.APIs.Gmail_API import GmailAPI

from dotenv import load_dotenv

load_dotenv()

gmail_api = GmailAPI()
mails = gmail_api.get_mails()
mailsString = "".join(mails)

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 1000,
    chunk_overlap  = 30,
    length_function = len,
    add_start_index = True,
)

docs = text_splitter.create_documents([mailsString])
print(docs[2].page_content)

# create embeddings
faiss_index = FAISS.from_documents(docs, OpenAIEmbeddings())

# save the index database
faiss_index.save_local("./Vector_DBs/kyrill_mails_1000_30")

# load the index database
db = FAISS.load_local("./Vector_DBs/kyrill_mails_1000_30", OpenAIEmbeddings())
faiss_index = db


# similarity search function
def retrieve_info(query):
    similar_documents = faiss_index.similarity_search(query, k=12)
    page_contents_array = [doc.page_content for doc in similar_documents]
    print(page_contents_array)
    return page_contents_array


# similarity search
query = "Schreibe eine Mail an deinen KI Professor"

# 2. Setup GPT and template
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")

template = """
    You are writing an Email based on the task provided.
    Your task/message is: {message}

    1/ Your answers should be in the style of your previouse answers provided here: {chats}
    2/ Always answer in a way that is matchesthe conversation.

    Please write the best response that you can.
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["message", "chats"]
)

chain = LLMChain(llm=llm, prompt=prompt)


# 3.Retrieval augmented generation
def generate_response(query):
    chats = retrieve_info(query)
    response = chain.run(chats=chats, message=query)
    return response


response = generate_response(query)
print(response)
