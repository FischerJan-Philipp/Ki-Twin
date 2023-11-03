from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class calendarAPI:
    def getData(self):
        creds = None
        if os.path.exists('../token.json'):
            creds = Credentials.from_authorized_user_file('../token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('./credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('../token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('calendar', 'v3', credentials=creds)
            # Get a list of all calendars
            calendar_list = service.calendarList().list().execute()

            # Create an empty list to accumulate event data
            event_data = []

            # Loop through each calendar and retrieve events
            for calendar in calendar_list.get('items', []):
                calendar_id = calendar['id']

                print(f"Getting events from calendar: {calendar['summary']}")

                now = datetime.datetime.utcnow().isoformat() + 'Z'
                events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                                      maxResults=50, singleEvents=True,
                                                      orderBy='startTime').execute()
                events = events_result.get('items', [])

                if events:
                    for event in events:
                        start = event['start'].get('dateTime', event['start'].get('date'))
                        end = event['end'].get('dateTime', event['end'].get('date'))
                        attendees = [attendee['email'] for attendee in event.get('attendees', [])]
                        print(start, event['summary'])

                        rowData = {'id': event['id'],
                                   'summary': event['summary'],
                                   'start': start,
                                   'end': end,
                                   'location': event.get('location', 'No location provided'),
                                   'description': event.get('description', 'No description provided'),
                                   'attendees': attendees
                                  }
                        event_data.append(rowData)

                # Create a DataFrame after the loop
                df = pd.DataFrame(event_data)
                df.to_csv(f'./Data/Calendar/{creds.client_id}.csv', index=False)

        except HttpError as error:
        print('An error occurred: %s' % error)

calendarAPI = calendarAPI()
calendarAPI.getData()
