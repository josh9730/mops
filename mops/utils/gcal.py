import pickle
import os
import keyring
from datetime import datetime, date
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GCal:
    def __init__(self, gcal_auth_path: str):
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
        creds = None
        if os.path.exists(f"{gcal_auth_path}token.pickle"):
            with open(
                f"{gcal_auth_path}token.pickle",
                "rb",
            ) as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f"{gcal_auth_path}credentials.json",
                    SCOPES,
                )
                creds = flow.run_local_server(port=0)

            with open(
                f"{gcal_auth_path}token.pickle",
                "wb",
            ) as token:
                pickle.dump(creds, token)
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
