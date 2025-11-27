from __future__ import print_function
import datetime
import os.path
import dateparser
import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
WIB = pytz.timezone("Asia/Jakarta")


def get_service():
    """Autentikasi Google Calendar dan menghasilkan service client."""
    creds = None

    # Cek token login
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Jika belum login / token expired
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Simpan token
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


# ========================
#  PARSING TANGGAL AMAN
# ========================

def parse_datetime_indonesia(text):
    """
    Mem-parse tanggal Indonesia dengan aman:
    - pakai tahun sekarang kalau tahun tidak disebutkan
    - pakai timezone Asia/Jakarta
    - prefer future date (besok lebih diutamakan daripada tahun depan)
    """

    dt = dateparser.parse(
        text,
        settings={
            'TIMEZONE': 'Asia/Jakarta',
            'PREFER_DATES_FROM': 'future',
            'RELATIVE_BASE': datetime.datetime.now()
        }
    )

    if not dt:
        return None

    # Jika dateparser memberi datetime timezone-aware → convert ke WIB
    if dt.tzinfo is not None:
        dt = dt.astimezone(WIB)
        dt = dt.replace(tzinfo=None)

    # Jika dateparser memberi tahun aneh → pakai tahun ini
    current_year = datetime.datetime.now().year
    if dt.year < current_year - 1 or dt.year > current_year + 1:
        dt = dt.replace(year=current_year)

    return dt


# ========================
#  LIST EVENTS
# ========================

def list_events(date_text):
    """Menampilkan agenda pada tanggal tertentu."""
    service = get_service()

    dt = parse_datetime_indonesia(date_text)
    if not dt:
        return "❌ Tanggal tidak bisa dipahami."

    start = WIB.localize(datetime.datetime(dt.year, dt.month, dt.day, 0, 0))
    end = start + datetime.timedelta(days=1)

    events_result = service.events().list(
        calendarId='primary',
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        return f"📭 Tidak ada agenda pada tanggal {dt.strftime('%d-%m-%Y')}."

    hasil = f"📅 Agenda pada {dt.strftime('%d-%m-%Y')}:\n"
    for event in events:
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        hasil += f"- {event['summary']} (mulai {start_time})\n"

    return hasil


# ========================
#  ADD EVENT
# ========================

def add_event(date_text, title):
    """Menambah agenda baru ke Google Calendar."""
    service = get_service()

    dt = parse_datetime_indonesia(date_text)
    if not dt:
        return "❌ Tanggal/jam tidak bisa dipahami."

    start = WIB.localize(dt)

    event = {
        'summary': title,
        'start': {'dateTime': start.isoformat()},
        'end': {'dateTime': (start + datetime.timedelta(hours=1)).isoformat()},
    }

    service.events().insert(calendarId='primary', body=event).execute()
    return f"✔️ Agenda '{title}' berhasil ditambahkan pada {start.strftime('%d-%m-%Y %H:%M')}."
