import os
import pickle
from datetime import date, datetime

import keyring
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GCal:
    def __init__(self, gcal_auth_path: str):
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
        creds = None

        if os.path.exists(f"{gcal_auth_path}/gcal_token.json"):
            creds = Credentials.from_authorized_user_file(
                f"{gcal_auth_path}gcal_token.json", SCOPES
            )
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:

                flow = InstalledAppFlow.from_client_secrets_file(
                    f"{gcal_auth_path}desktop_oauth_gcal.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(f"{gcal_auth_path}gcal_token.json", "w") as token:
                token.write(creds.to_json())

        try:
            self.service = build("calendar", "v3", credentials=creds)

        except HttpError as error:
            print("An error occurred: %s" % error)

        self.service = build("calendar", "v3", credentials=creds)
        self.internal_cal_url = keyring.get_password("internal_cal", "url")

    def create_calendar_event(self, *args: str):
        """Creates Internal Calendar Event

        Args:
            start_time (str): start time (military)
            end_time (str): end time (military)
            day (str): day (can be 'today')
            title (str): title for the event
        """
        start_day = (
            date.today() if args[2] == "today" else date.fromisoformat(str(args[2]))
        )

        start_hour = int(args[0][0:2])
        start_min = int(args[0][2:4])
        end_hour = int(args[1][0:2])
        end_min = int(args[1][2:4])

        start_iso = datetime(
            start_day.year, start_day.month, start_day.day, start_hour, start_min
        ).isoformat()
        end_iso = datetime(
            start_day.year, start_day.month, start_day.day, end_hour, end_min
        ).isoformat()

        # Create calendar dict to create event
        body = {
            "summary": args[3],
            "start": {"timeZone": "America/Los_Angeles", "dateTime": start_iso},
            "end": {"timeZone": "America/Los_Angeles", "dateTime": end_iso},
        }

        self.service.events().insert(
            calendarId=self.internal_cal_url,
            body=body,
        ).execute()
