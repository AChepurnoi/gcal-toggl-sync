import logging
import datetime
from gcal import CliCalendarService, Event
from toggl import TogglService

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    day = datetime.date(2019, 11, 1)
    
    calendar = CliCalendarService()
    events = calendar.fetch_events(day)

    with open('toggl_token.txt') as token_file:
        toggl_token = token_file.read()
        
    toggl = TogglService(toggl_token)
    toggl.persist_events(day, events)