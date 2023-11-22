# Ki-Twin

## Directory: Prof Project
Run with `streamlit run UI_prof.py`

- `chat_with_prof.py`: Contains the logic of the chatbot.
- `pdf_Summarizer`: Summarizes Lectures Script with GPT-4 vision.
- `prof_transcription.py`: Transcribes an online lecture mp3 file (English) with Whisper.
- `prof_vectorDB.py`: Creates vector DB with Faiss out of the transcript.
- `slides_to_vectorDB.py`: Creates vector DB with Faiss for the slides summaries from `pdf_Summarizer.pdf`.

## AI Clone
Run with `streamlit run UI.py`

- `calendar_chat.py`: Contains the logic of the chatbot.
  - Retrieves relevant date timeframe for the query input with gpt-3.5-turbo function.
  - Sends prompt with the appointments in the calendar and the retrieved chats from the vector DB for our downloaded WhatsApp chats, to imitate the writing style.

## Sources/APIs
- Google APIs for getting all sent Emails in Gmail, all Google Calendar events, and all Google Drive documents.
- We tested with all but in the final projects we only used the Google Calendar events for the "AI Clone".
  - Gmail Data is good for imitating E-Mail style and Drive Documents are good (in our case) for creating notes, writing applications, CVs etc.

## Sources/Data
- Data used for the projects and tests.
- `Chat` has the text file used for our chat vector DB.
- `Prof` has the transcript, the script of the module as pdf and under `Slides` the text files of the summarized slides.
- `Calendar` has a csv file that was created with the `calendarAPI.py` (test events created just for showcase here in the repo).

## Sources/Prompt_Templates
- Prompt template for the AI Clone and for the Prof Clone.

## Sources/Vector_DBs
- Vector DBs tested and used for the projects and test.
- We deleted some because of private data.

## Sprints
- Just our first files and first steps.
