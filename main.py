import logging
import datetime
from gcal import CliCalendarService, Event
from toggl import TogglService, LocalFSTokenStore
import os
import sys

import argparse
from config import resource_path

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', "--date",
                        help="The date to sync - format YYYY-MM-DD",
                        type=datetime.date.fromisoformat,
                        default=datetime.date.today())
    parser.add_argument("-t", "--token", type=str, default=None, help="Toggl token")
    parser.add_argument("-w", "--workspace", type=str, default="1059890", help="Toggl workspace id")
    args = parser.parse_args()

    logging.info(f"========= Initializing =========")
    token_store = LocalFSTokenStore(token_init=args.token)
    calendar = CliCalendarService()
    toggl = TogglService(token=token_store.token, workspace_id=args.workspace)

    logging.info(f"========= Starting synchronization for {args.date} =========")
    events = calendar.fetch_events(args.date)
    toggl.persist_events(args.date, events)