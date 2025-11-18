import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def list_events(calendarId="primary"):
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
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
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId=calendarId,
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])

  except HttpError as error:
    print(f"An error occurred: {error}")
    

def list_calenderID():
    #fix crendentials to access the google API
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
   
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
        creds = flow.run_local_server(port=0)
   
    with open("token.json", "w") as token:
        token.write(creds.to_json())
        
        
    # access the google calendar API to list calendar IDs
    try:
        service = build("calendar", "v3", credentials=creds)
               
        calender_list=service.calendarList().list().execute()
        for calendar_entry in calender_list['items']:
            print(f"Calendar Summary: {calendar_entry['summary']}, ID: {calendar_entry['id']}")     
        return calender_list

    except HttpError as error:
        print(f"An error occurred: {error}")

def add_event(details):

    #fix crendentials to access the google API
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
   
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
        creds = flow.run_local_server(port=0)
   
    with open("token.json", "w") as token:
        token.write(creds.to_json())
        
        
    try:
        service = build("calendar", "v3", credentials=creds)
               
        event = {
          'summary': details['summary'],
          'location': details['location'],
          'description': details['description'],
          'start': {
            'dateTime': details['start_datetime'],
            'timeZone': details['time_zone'],              
            },
            'end': {
            'dateTime': details['end_datetime'],
            'timeZone': details['time_zone'],
            },
            'recurrence': details['recurrence'],
            'attendees': details['attendees'],
            'reminders': {
            'useDefault': True,       
            },
        }       
        event = service.events().insert(calendarId=details['calenderID'], body=event).execute()
        print ('Event created: %s' % (event.get('htmlLink')))
        
        
        
    except HttpError as error:
        print(f"An error occurred: {error}")

    
if __name__ == "__main__":
    # print("listing calendar IDs, please select one to list events from:")
    # calender_list=list_calenderID()
    
    # for el in range(len(calender_list['items'])):
    #     print(f"Enter {el+1} for calendar ID: {calender_list['items'][el]['summary']}")
    # print("Enter 0 to exit.")
    # selected_calendarId=input("Please enter the calendar ID from the list above: ")
    # while int(selected_calendarId) not in range(0,len(calender_list['items'])+1):
    #     selected_calendarId=input("Invalid selection. Please enter a valid calendar ID from the list above or 0 to exit: ")
    # if int(selected_calendarId)==0:
    #     exit()
    # else:
    #     calendarId=calender_list['items'][int(selected_calendarId)-1]['id']
    #     print(f"Listing events for calendar ID: {calendarId}")
    #     list_events(calendarId=calendarId)
    details={
    'summary':'Google I/O 2024',
    'location':'800 Howard St., San Francisco, CA 94103',
    'description':'A chance to hear more about Google\'s developer products.',          
    'start_datetime':'2025-05-28T09:00:00-07:00',
    'end_datetime':'2025-05-28T17:00:00-07:00',
    'time_zone':'America/Los_Angeles',
    'recurrence':['RRULE:FREQ=DAILY;COUNT=2'],
    'attendees':[{'email':'test@gmail.com'}],
    'calenderID':'primary'
    }
    add_event(details)
