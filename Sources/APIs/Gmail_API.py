import os.path
import base64
import email
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup

class GmailAPI:
  def __init__(self):
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "../../credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(creds.to_json())

    self.service = build("gmail", "v1", credentials=creds)

  def get_mails(self):

    try:
      # Call the Gmail API
      mails = self.service.users().messages().list(userId='me', q="label:sent").execute()
      messages = mails.get("messages", [])

      print("MESSAGES: ", messages)
      print(len(messages))
      mailList = []
      for msg in messages:
        # Get the message from its id
        txt = self.service.users().messages().get(userId='me', id=msg['id']).execute()

        # Use try-except to avoid any Errors
        try:
          # Get value of 'payload' from dictionary 'txt'
          payload = txt['payload']
          headers = payload['headers']
          header_str = str(headers)

          # Check if the body contains 'data'
          if 'data' in payload['body']:
            body = payload['body']['data']
          else:
            # If not, look for the data in 'parts'
            parts = payload.get('parts', [])
            if parts:
              # Get the 'data' from the first part
              body = parts[0]['body']['data']
            else:
              # If there are no parts, skip this message
              continue

          decoded_data_str = base64.urlsafe_b64decode(body).decode('utf-8')
          combined_data = header_str + "\n\n" + decoded_data_str
          mailList.append(combined_data)
          # rest of your code
        except Exception as e:
          print(f"An error occurred while processing message {msg['id']}: {e}")
      return mailList
    except HttpError as error:
      # TODO(developer) - Handle errors from gmail API.
      print(f"An error occurred: {error}")
