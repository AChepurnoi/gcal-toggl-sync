import datetime
from gcal import Event
from base64 import b64encode
import logging
from typing import Tuple, List, Type
import requests
import os
from config import LOCAL_STORAGE_PATH

class TogglAPI:
    def __init__(self, token: str, base_url='https://toggl.com'):
        self._token = token
        self._base_url = base_url
        auth_header = self._token + ":" + "api_token"
        self._auth_header_value = "Basic " + b64encode(auth_header.encode()).decode('ascii').rstrip()

    def _auth_header(self) -> Tuple[str, str]:
        return 'Authorization', self._auth_header_value

    def _get(self, url: str, params=None):
        auth_header, auth_val = self._auth_header()
        req = requests.get(self._base_url + url, params=params, headers={auth_header: auth_val})
        return req

    def _post(self, url: str, json):
        auth_header, auth_val = self._auth_header()
        req = requests.post(self._base_url + url, headers={auth_header: auth_val}, json=json)
        return req
    
    def workspaces(self):
        res = self._get('/api/v8/workspaces').json()
        return res

    def time_entries(self, params):
        res = self._get('/api/v8/time_entries', params=params)
        return res.json()

    def projects(self, space_id: int):
        res = self._get('/api/v8/workspaces/{}/projects'.format(space_id)).json()
        return res
    
    def create_entry(self, params):
        res = self._post('/api/v8/time_entries', json=params)
        return res.json()


class LocalFSTokenStore():
    def __init__(self, store_name="toggl_token", token_init=None):
        if token_init:
            self.token = token_init
            with open(f'{LOCAL_STORAGE_PATH}/{store_name}.txt', 'w') as token_store:
                token_store.write(self.token)
        elif os.path.exists(f'{LOCAL_STORAGE_PATH}/{store_name}.txt'):
            with open(f'{LOCAL_STORAGE_PATH}/{store_name}.txt', 'r') as token_store:
                self.token = token_store.read()
        else: 
            logging.error(f"Token not found. Please provide token and it will be saved for sequential use (Storage path: {LOCAL_STORAGE_PATH})")
            raise FileNotFoundError("Token not found")


class TogglService:
    def __init__(self, token: str, workspace_id):
        self._api = TogglAPI(token=token)
        self._wid = workspace_id

    def _duplicate_event_filter(self, existing_entries):
        def filter(event: Event):
            for entry in existing_entries:
                start_time = datetime.datetime.fromisoformat(entry['start'])
                if event.start == start_time and event.duration == int(entry['duration']):
                    logging.info(f"Skipping time entry for \"{event.summary}\"")
                    return False
            return True
        return filter

    def persist_events(self, day: datetime.date, events: List[Type[Event]]):
        if len(events) == 0:
            logging.warning("No events passed")
            return 
        existing_entries = self._api.time_entries({
            'start_date': datetime.datetime(day.year, day.month, day.day, 0, 0).isoformat() + 'Z',
            'end_date': datetime.datetime(day.year, day.month, day.day, 23, 59).isoformat() + 'Z'
        })

        events = list(filter(self._duplicate_event_filter(existing_entries), events))

        for event in events:
            logging.info(f"Adding time entry for \"{event.summary}\"")
            self._api.create_entry({
                'time_entry': {
                    'wid': self._wid,
                    'description': event.summary,
                    'start': event.start.isoformat(),
                    'duration': event.duration,
                    'created_with': 'gcal-toggl'
                }
            })

        logging.info(f"Created {len(events)} events")
