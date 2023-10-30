from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class DriveAPI:
    def getData(self):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('../token.json'):
            creds = Credentials.from_authorized_user_file('../token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '../credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('../token.json', 'w') as token:
                token.write(creds.to_json())
        textFiel = []
        try:
            service = build('drive', 'v3', credentials=creds)

            # Call the Drive v3 API
            results = service.files().list(
                pageSize=100, fields="nextPageToken, files(id, name, mimeType)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id'], item['mimeType']))
                print(item['mimeType'])
                if(item['mimeType'] == 'application/vnd.google-apps.document'):
                    textFiel.append(service.files().export(fileId=item['id'], mimeType="text/plain").execute())

        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')

        #file = service.files().export(fileId='1WKOiHDF6-gw1CC1XrSmatjwAjUK3Ou2ci1SigDk4xlM', mimeType="text/plain").execute()
        for index, field in enumerate(textFiel):
            filename = f"Data/{index}.txt"  # You can use the index to create unique filenames
            with open(filename, "w", encoding="utf-8") as text_file:
                text_file.write(field.decode("utf-8"))  # Assuming field is in bytes
                print(f"Saved {filename}")
        print("_____________________________")
        print(textFiel)
        print("_____________________________")
        print(len(textFiel))


driveAPI = DriveAPI()
driveAPI.getData()