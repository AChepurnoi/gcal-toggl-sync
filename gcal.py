
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from base64 import b64encode
import logging

class Event:
    def __init__(self, summary: str, start: datetime.datetime, end: datetime.datetime):
        self.summary = summary
        self.start = start
        self.end = end
        self.duration = int((end - start).total_seconds())
    
    def __str__(self):
        return f"{self.summary} event [{self.start} - {self.end}] ({self.duration}s)"



# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
class CliCalendarService:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self._service = build('calendar', 'v3', credentials=creds)
    
    def fetch_events(self, day: datetime.date):
        startTime = datetime.datetime(day.year, day.month, day.day, 0, 0, 0).isoformat() + 'Z'
        endTime = datetime.datetime(day.year, day.month, day.day, 23, 59, 59).isoformat() + 'Z'
        events_result = self._service.events().list(calendarId='primary', 
                                              timeMin=startTime,
                                              timeMax=endTime,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        result = []
        for event in events:
            summary = event['summary']
            if event['status'] != 'confirmed':
                logging.info("Skipping event(Wrong status): {summary}")
                continue

            startTime = datetime.datetime.fromisoformat(event['start'].get('dateTime', None))
            if startTime is None:
                logging.info("Skipping event(Full day): {summary}")
                continue

            start = startTime.astimezone(tz=datetime.timezone.utc)
            end = datetime.datetime.fromisoformat(event['end'].get('dateTime', None)).astimezone(tz=datetime.timezone.utc)
            result.append(Event(summary=summary,start=start, end=end))
        
        return result


